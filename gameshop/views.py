from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist,SuspiciousOperation
import json

from datetime import datetime,date
from django.utils import timezone

from django.http import JsonResponse
from django.db.models import F, FloatField, Sum

"""form.fields['redirect_url'].widget = forms.HiddenInput()"""

from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import RegistrationForm, LoginForm, GameForm, userForm,profileForm
from storefront.models import Profile, Developers, Game, API_AUTH
from django.db.models import Sum
from django.utils.crypto import get_random_string
from django.core import mail
from django.conf import settings

from django.contrib import messages
from django.core.mail import send_mail
from api.views import get_hashed_check_sum
from django.core.urlresolvers import reverse
import urllib


def send_validation_request_email(request, user):

    to = user.email
    timestamp =  int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    token = get_hashed_check_sum(user.username,timestamp,user.password,0)

    protocol = "https://" if request.is_secure else "http://"
    url = request.build_absolute_uri('/email/validate')
    link = str(url+'?ref='+ str(user.id) +'&ts='+str(timestamp)+'&token='+token)


    with mail.get_connection() as connection:
        subject = "Vadiate your email"
        body = "Thank you for registering on awesome-game-shop.com<br>"
        body += "Please click on the link below to validate your email address and activate your account<br>"
        body +="<a href=\""+link+"\"> click Hear</a><br>"
        body += "if link doesn't work past the following address to the browser <br>"
        body += link + "<br>"

        body +="Best Regards,<br>"

        msg = mail.EmailMessage(
            subject, body, settings.EMAIL_HOST_USER, [to],
            connection=connection,
        )
        msg.content_subtype = "html"
        msg.send()

def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

def email_validator(request):
    if request.method == 'GET':
        try:
            ref = request.GET.get('ref')
            timestamp = int(request.GET.get('ts'))
            token = request.GET.get('token')


            receiving_time =  int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
            if receiving_time - timestamp > settings.EMAIL_VALIDATION_REQUEST_MAX_DELAY: #if timestamp is older reject
                raise SuspiciousOperation
            if receiving_time -timestamp < 0:
                raise SuspiciousOperation

            user_object = User.objects.get(id = int(ref))

            checksum = get_hashed_check_sum(user_object.username,timestamp,user_object.password,0)

            if checksum != token:
                raise SuspiciousOperation
            else:
                user_object.profile.email_vaidated = True
                user_object.save()
                return custom_redirect('login', msg = 'Your account is activated, you can now login')

        except ObjectDoesNotExist:
            info = {
                'alert_type':"'alert alert-danger alert-dismissable'",
                'title':'Validate your email',
                'msg':["Email validation failed",
                 'make sure if you have used the correct email link',

                 ]
            }
            return render(request,'messages.html',{'info':info})
        except SuspiciousOperation:
            info = {
                'alert_type':"'alert alert-danger alert-dismissable'",
                'title':'Validate your email',
                'msg':["Email validation failed",
                 'make sure if you have used the correct email link',
                 'make sure to use the link within 20 minute after it was send'
                 ]
            }
            return render(request,'messages.html',{'info':info})



def resend_validation_email(request):
    ref = request.GET.get('ref')
    try:
        user_object = User.objects.get(id = int(ref))
        send_validation_request_email(request, user_object)
        info = {
        'alert_type':"'alert alert-info alert-dismissable'",
        'title':'Validate your email',
        'msg':["Thank you for registering on awesome-game-shop.com",
         'An email has been sent to your email account. please use the provided link to activate your account',
         ],
         'ref':user_object.id
        }
    except ObjectDoesNotExist:
        info = {
            'alert_type':"'alert alert-danger alert-dismissable'",
            'title':'Validate your email',
            'msg':["Fatal error: Can not find object",
             ],
             'ref':user_object.id
        }
        return render(request,'messages.html',{'info':info})

    return render(request,'messages.html',{'info':info})


class LoginFormView(View):
    form_class = LoginForm

    def get(self,request):
        form = self.form_class(None)

        redirect_url    = request.GET.get('next')
        message         = request.GET.get('msg')
        if message is not None:
            info = {'msg':message}
        else:
            info = None

        if redirect_url ==  None :
            redirect_url    = request.path

        return render(request,'login.html',{'form':form, 'redirect_url':redirect_url,'info':info})

    def post(self,request):

        form = self.form_class(request.POST)
        error_msg = None

        if form.is_valid():
            username        = form.cleaned_data['username']
            password        = form.cleaned_data['password']
            redirect_url    = request.GET.get('next')

            if redirect_url ==  None :
                redirect_url = 'storefront:index'

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    if user.profile.email_vaidated:
                        login(request,user)
                        return redirect(redirect_url)
                    else:
                        info = {
                        'alert_type':"'alert alert-danger alert-dismissable'",
                        'title':'Validate your email',
                        'msg':["Your account is not activated",
                         'An email was sent to your email account. please use the provided link to activate your account',
                         ],
                         'ref':str(user.id)
                        }
                        return render(request,'messages.html',{'info':info})
                else:
                    error_msg = "inactive account"
            else:
                error_msg = "invalid username or password"
        else:
            error_msg = "validation error"

        return render(request,'login.html',{'form':form,'error_msg':error_msg})

class RegistrationFormView(View):
    form_class = RegistrationForm

    def get(self,request):
        form = self.form_class(None)
        return render(request,'register.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        error_msg = None
        if form.is_valid():
            user = form.save(commit = False)

            username    = form.cleaned_data['username']
            email       = form.cleaned_data['email']
            first_name  = form.cleaned_data['first_name']
            last_name   = form.cleaned_data['last_name']
            password    = form.cleaned_data['password']
            user.set_password(password)
            user.active = False
            user.save()

            user = authenticate(username=username,password=password)
            if user is not None:
                    send_validation_request_email(request, user)
                    info = {
                    'alert_type':"'alert alert-success alert-dismissable'",
                    'title':'Validate your email',
                    'msg':["Thank you for registering on awesome-game-shop.com",
                     'An email has been sent to your email account. please use the provided link to activate your account',
                     ],
                     'ref':str(user.id)

                    }

                    return render(request,'messages.html',{'info':info})
            else:
                error_msg = "try again"

        return render(request,'register.html',{'form':form,'error_msg':error_msg})

def generate_token(user):
    token = API_AUTH(user=user,
                     sid = get_random_string(20),
                     skey= User.objects.make_random_password(100)
                    )
    token.save()
    return token.sid, token.skey;




class ProfileView(LoginRequiredMixin, View):
    login_url       = '/login/'
    form_class      = userForm
    profile_form    = profileForm

    def get(self,request):

        user_object = User.objects.get(id = request.user.id)
        profile_img_path = user_object.profile.profile_img_path
        try:
            games = user_object.profile.games.all()


        except ObjectDoesNotExist:
            games = None

        form = self.form_class(None)
        image_form = self.profile_form(profile_img_path)

        try:
            token = API_AUTH.objects.get(user=user_object)
            sid = token.sid;
            skey = token.skey;

        except ObjectDoesNotExist:
            sid, skey = generate_token(user_object);

        data = {'username':request.user.username,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'email':request.user.email,
                'sid':sid,
                'skey':skey}

        contributions = None
        sales = None
        error_msg = None

        try:
            if user_object.developers.active :
                contributions = user_object.developers.game_set.all()
        except ObjectDoesNotExist:
            contributions = None
            sales = None

        try:
            sales = user_object.developers.payments_set.all()
            total = sales.aggregate(total_sales=Sum(F('paid_amount'), output_field=FloatField()))
            total_sales = total['total_sales']
        except ObjectDoesNotExist:
            sales = None
            total_sales = 0

        return render(request,'profile.html',{'form':form,
                                                'image_form':image_form,
                                                'profile_img_path':profile_img_path,
                                                'data':data,
                                                'error_msg':error_msg,
                                                'games':games,
                                                'contributions':contributions,
                                                'sales':sales,
                                                'total':total_sales,

                                                })

    def post(self,request):
        user_object = User.objects.get(id = request.user.id)
        profile_img_path = user_object.profile.profile_img_path

        form = self.form_class(request.POST, instance=user_object)

        if form.is_valid():
            user = form.save(commit = False)

            username    = form.cleaned_data['username']
            email       = form.cleaned_data['email']
            first_name  = form.cleaned_data['first_name']
            last_name   = form.cleaned_data['last_name']
            user.save()

            context = {
                 "message": 'update successful',
            }

            return HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
        else:

            context = {
                'message': 'could not process request due to form validation error',
                'errors' : form.errors,
            }
            response = HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
            response.status_code = 400

            return response



@login_required(login_url="/login/")
def image_upload(request):
    if request.method == 'POST':

        user_object = User.objects.get(id = request.user.id)
        profile  = user_object.profile

        file_path = user_object.profile.profile_img_path.url
        form = profileForm(request.POST, request.FILES, instance = profile)

        if form.is_valid():
            user_profile = form.save(commit = False)
            user_profile.save()

            context = {
                 "message": 'update successful',
                 "path": file_path,
            }

            return HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
        else:

            context = {
                'message': 'could not process request due to form validation error',
                'errors' : form.errors,
            }
            response = HttpResponse(
                json.dumps(context),
                content_type="application/json"
            )
            response.status_code = 400

            return response
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



#The form for adding a new game and editing information to an existing game added by the developer.
class GameFormView(LoginRequiredMixin,View):
    form_class = GameForm
    def get(self,request,game_id=None):
        #Edit the game. Checking that the game exists and that the developer owns the game.
        if game_id:
            game = get_object_or_404(Game, id=game_id)
            print(game.developer.user)
            print(request.user)
            if game.developer.user != request.user:
                return HttpResponseForbidden()
        #Adding a new game.
        else:
            game = Game()
        form = self.form_class(None, instance=game)
        return render(request,'addgame.html',{'form':form})

    def post(self,request,game_id=None):
        if game_id:
            game = get_object_or_404(Game, id=game_id)
            print(game.developer.user)
            print(request.user)
            if game.developer.user != request.user:
                return HttpResponseForbidden()
        else:
            game = None
        form = self.form_class(request.POST, request.FILES, instance=game)
        error_msg = None
        if form.is_valid():
            game = form.save(commit = False)

            #Making the user a developer for the game.
            user_object = User.objects.get(id = request.user.id)
            if(hasattr(user_object, 'developers')):
                game.developer = user_object.developers
            else:
                user_object.developers = Developers(user = user_object,
                                                active = True)
                user_object.developers.save()
                game.developer = user_object.developers
            game.save()

            #Developers should own their own games.
            user = User.objects.get(id = request.user.id)
            user.profile.games.add(game)
            user.save()

            return redirect('storefront:game_detail', game_id=game.id)
        else:
            return render(request,'addgame.html',{'form':form,'error_msg':error_msg})

#A developer can delete a game they have added.
@login_required(login_url="/login/")
def delete_game(request,game_id):
    if request.method == 'POST':
        user_object = User.objects.get(id = request.user.id)
        game_object = Game.objects.get(id = game_id)
        if user_object == game_object.developer.user:
            game_object.delete()
            return redirect('profile')
    return HttpResponseForbidden()


def logout(request):
    auth.logout(request)
    return redirect('storefront:index')



def social_callback(request):
    redirect_url    = request.GET.get('next')
    if user.is_authenticated and backends.associated :
        return redirect(redirect_url)
    else:
        auth.logout(request)
        return redirect('/login')
