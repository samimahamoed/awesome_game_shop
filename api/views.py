from django.shortcuts import render,get_object_or_404
from django.core import serializers
from django.http import HttpResponse,HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist,SuspiciousOperation
import json
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from django.conf import settings
from django.contrib.auth.models import User
from storefront.models import Game,Highscore


from .forms import token_regenerate_form
from storefront.models import API_AUTH
from django.utils.crypto import get_random_string
import re
from hashlib import md5
from datetime import datetime,date
from django.utils import timezone


def get_hashed_check_sum(arg1, arg2, token,select):

    checksumstr = {
           0:"{}:{}:{}".format(arg1, arg2,token),
           1:"{}:{}".format(arg1, arg2)
    }

    m = md5(checksumstr[select].encode("ascii"))
    return m.hexdigest()


def api_authentication_required(function=None, home_url=None, redirect_field_name=None):
    """decorator fuction to authenticate api request using digest authentication method.
    The request should cointain authentication header
    with the following parameters
        username: secret id which can be accessed through profile page
        realm: any value with (string and number only, no special character)
        nonce:unix epoch timestamp generated as utc timezone
        response:checksum using MD5 algorithm

        password: secret key which can also be found via profile page

    the checksum will be caculated as follows


    #acceptable algorithm directive's value is "MD5 so we calculate HA1 as follows
    HA1=MD5(username:realm:password)

    #acceptable qop directive's value is null(unspecified), then HA2 is
    HA2=MD5(method:digestURI)

    #thus since the qop directive is unspecified,we calculate the response as follows
    response=MD5(HA1:nonce:HA2)
    """


    def _dec(view_func):
        def _view(request, *args, **kwargs):

            try:
                auth_headers = request.META.get('HTTP_AUTHORIZATION')
                reg=re.compile('(\w+)[:=] ?"?(\w+)"?')
                header_values = dict(reg.findall(auth_headers))   # Parse header values

                request_receiving_time_epoch =  datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
                request_sending_time_epoch   = int(header_values['nonce'])
                if request_receiving_time_epoch-request_sending_time_epoch > settings.API_REQUEST_MAX_DELAY:
                    raise SuspiciousOperation
                if request_receiving_time_epoch-request_sending_time_epoch < 0: #if timestamp is older reject
                    raise SuspiciousOperation

                token = API_AUTH.objects.get(sid=header_values['username'])

            except ObjectDoesNotExist:
                context = {
                    'message': "Object Does Not Exist, try again",
                }
                response = HttpResponse(
                    json.dumps(context),
                    content_type="application/json"
                )
                response.status_code = 400
                return response;
            except SuspiciousOperation:
                context = {
                    'message': "old timestamp, try again",
                }
                response = HttpResponse(
                    json.dumps(context),
                    content_type="application/json"
                )
                response.status_code = 400
                return response;


            #acceptable algorithm directive's value is "MD5 so we calculate HA1 as follows
            HA1 = get_hashed_check_sum(header_values['username'],header_values['realm'],token.skey,0)

            #acceptable qop directive's value is null(unspecified), then HA2 is
            HA2 = get_hashed_check_sum(request.method,request.path,0,1)

            #thus since the qop directive is unspecified,we calculate the response as follows
            response = get_hashed_check_sum(HA1,header_values['nonce'],HA2,0)



            if response != header_values['response']:
                context = {
                    "calculated checksum":response,
                    "received checksum": header_values['response'] ,
                     "HA1":HA1,
                     "HA2":HA2 ,
                     'realm':header_values['realm'],
                     'nonce':header_values['nonce'],
                     'username':header_values['username']
                }
                response = HttpResponse(
                    json.dumps(context),
                    content_type="application/json"
                )
                response.status_code = 400
                return response;
            else:
                return view_func(request, *args, **kwargs)


        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)




@login_required(login_url="/login/")
@csrf_protect
def regenerate_token(request):

    if request.method == 'POST':
        user_object = User.objects.get(id = request.user.id)
        error_msg = "post in"

        #sid = user_object.API_AUTH.sid;
        error_msg+="try in"
        received_sid = request.POST['sid'].replace('Secret id:','');

        error_msg = received_sid



        try:
            error_msg+="sid in"
            token = API_AUTH.objects.get(sid=received_sid)
        except ObjectDoesNotExist:
            context = {
                'message': '',
            }
            response = HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
            #in this case object must exist unless the sid is altered, so we reply badrequest
            response.status_code = 400
            return response;

        token.sid  = get_random_string(20)
        token.skey = User.objects.make_random_password(100)
        token.save()

        context = {
             "message": {'sid':token.sid,'skey':token.skey, 'result':'token updated'},
        }

        return HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )




def Index(request):
        context = {
            'message': 'Bad request',
        }
        response = HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )
        response.status_code = 400

        return response

@api_authentication_required
def sales(request,game_id=None):
    auth_headers = request.META.get('HTTP_AUTHORIZATION')
    reg=re.compile('(\w+)[:=] ?"?(\w+)"?')
    header_values = dict(reg.findall(auth_headers))   # Parse header values

    try:
        token = API_AUTH.objects.get(sid=header_values['username'])
        user_object = token.user

        sales = user_object.developers.payments_set.all()

        response = serializers.serialize("json", sales)


        return HttpResponse(
            response,
            content_type = 'application/json; charset=utf8'
        )

    except ObjectDoesNotExist:
        context = {
            'message': '',
        }
        response = HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )
        #in this case object must exist unless the sid is altered, so we reply badrequest
        response.status_code = 400
        return response;




def Games(request,game_id=None):

    if request.method == 'GET':

        if game_id == None:
            result = Game.objects.all().values('id',
                                                'name',
                                                'description',
                                                'image',
                                                'developer',
                                                'price',
                                                ).order_by('id')
        else:
            result = Game.objects.filter(id=game_id).values('id',
                                                                'name',
                                                                'description',
                                                                'image',
                                                                'developer',
                                                                'price',
                                                                )

        return HttpResponse(
            json.dumps(list(result)),
            content_type = 'application/json; charset=utf8'
        )

    else:

        context = {
            'message': 'Bad request',
        }
        response = HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )
        response.status_code = 400

        return response




def scores(request, game_id=None):

    if request.method == 'GET':
        limit = request.GET.get('limit')
        if limit is None:
            limit = 5

        if game_id is None:
            result = Highscore.objects.all()#.order_by('-game').order_by('-score')[:limit];
            response = serializers.serialize("json", result)
        else:
            game = get_object_or_404(Game, pk=game_id)
            result = Highscore.objects.filter(game = game).order_by('-score')[:limit];
            response = serializers.serialize("json", result)

        return HttpResponse(
            response,
            content_type = 'application/json; charset=utf8'
        )

    else:

        context = {
            'message': 'Bad request',
        }
        response = HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )
        response.status_code = 400

        return response
