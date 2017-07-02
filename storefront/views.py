from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Game, Payments, GameRating, Gamestate, Highscore
from hashlib import md5
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.clickjacking import xframe_options_exempt
import time
from .forms import GameRatingForm
import json

from django.db.models import Avg, Sum
from itertools import chain
# Create your views here.


def index(request):
    all_games = Game.objects.all()

    context = {
        'games': all_games,
        'search_enable':True,
    }
    return render(request,'index.html',context)


def search_games(request):
    if request.method == 'POST':
        value = request.POST.get('game_search')
    else:
        value = request.GET.get('game_search')

    games_by_name = Game.objects.filter(name__contains = value).order_by('-name');
    games_by_description = Game.objects.filter(description__contains = value).order_by('-description');

    result_list = list(chain(games_by_name, games_by_description))
    context = {
        'games': result_list,
        'search_enable':True,
    }
    return render(request,'games.html',context)

#Listing all games in games.html page.
def games(request):

    all_games = Game.objects.all()

    for game in all_games:
        try:
            game_rating = game.gamerating_set.all().aggregate(Avg('rating'))
            game.rating = game_rating['rating__avg']
        except  ObjectDoesNotExist:
            game.rating = 0


    context = {
        'games': all_games,
        'search_enable':True,
    }
    return render(request,'games.html',context)

def get_user_discount(current_user):
    return 0;

def get_hashed_check_sum(pid, arg2, arg3, token,select):

    checksumstr = {
           0:"pid={}&sid={}&amount={}&token={}".format(pid, arg2, arg3, token),
           1:"pid={}&ref={}&result={}&token={}".format(pid, arg2, arg3, token)
    }

    m = md5(checksumstr[select].encode("ascii"))
    return m.hexdigest()

@login_required(login_url="/login/")
def game_detail(request, game_id):
    error_msg = None
    info_msg = None
    is_game_already_paid = False

    game = get_object_or_404(Game, pk=game_id)

    highscores = Highscore.objects.filter(game = game).order_by('-score');

    if request.user.is_authenticated:

        user_object = User.objects.get(id = request.user.id)
        profile  = user_object.profile

        try:
            user_games = user_object.profile.games.all()
            if user_games.filter(id=game.id).exists():
                is_game_already_paid = True
        except  ObjectDoesNotExist:
            is_game_already_paid = False

        pid = str(time.time()) +'-'+ str(game.id)
        sid =  settings.PAYMENT_SELLER_ID  #TODO: is this safe ? the value is stored as enviroment variable
        discount = get_user_discount(request.user)
        amount = game.price - get_user_discount(request.user)
        token= settings.PAYMENT_SECRET_KEY  #TODO: is this safe ? the value is stored as enviroment variable

        try:
          #this is passed error message when page is redirected from other view due to failure
          error_msg = request.session.pop('error_msg')
        except:
          error_msg = None


        try:
        #this is passed info type message when page is redirected from other view
          info_msg = request.session.pop('info_msg')
        except:
          info_msg = None

        rating = 0

        try:
            game_rating = game.gamerating_set.all().aggregate(Avg('rating'))
            rating = game_rating['rating__avg']
        except  ObjectDoesNotExist:
            rating = 0


        for score in highscores:
            player = User.objects.get(id = score.player.id)
            score.player_nickname = player.username

        context ={
            'game': game,
            'game_already_paid':is_game_already_paid,
            'error_msg':error_msg,
            'info_msg':info_msg,
            'rating':rating,
            'highscores':highscores,
        }

        context['payment'] = { 'pid':pid,
                    'sid':sid,
                    'discount':discount,
                    'amount':amount,
                    'checksum':get_hashed_check_sum(pid,sid,amount,token,select = 0),
                  }

    return render(request, 'game_detail.html', context)

#Highscores in play.html are updated using ajax calls when better scores are saved.
@login_required(login_url="/login/")
def ajax_highscores(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    highscores = Highscore.objects.filter(game = game).order_by('-score')[:5];

    try:
        personal_highscore = Highscore.objects.get(player__user = request.user, game=game)
    except ObjectDoesNotExist:
        personal_highscore = None

    return render(request,'highscore.html',{'highscores':highscores,
                                        'personal_highscore':personal_highscore
                                        })



class Play(LoginRequiredMixin, View):
    login_url       = '/login/'
    form_class      = GameRatingForm


    def get(self,request, game_id):


        game = get_object_or_404(Game, pk=game_id)
        user_object = User.objects.get(id = request.user.id)
        profile  = user_object.profile
        user_game = None
        is_paid = False
        error_msg = None

        rating = 0

        try:
            user_games = user_object.profile.games.all()
            if user_games.filter(id=game.id).exists():
                is_paid = True
        except  ObjectDoesNotExist:
            is_paid = False
            error_msg = "you don't have access to this game"

        # Generating high scores for the game.
        highscores = Highscore.objects.filter(game = game).order_by('-score')[:5];

        # Checking if personal highscore exists.
        try:
            personal_highscore = Highscore.objects.get(player__user = request.user, game=game)
        except ObjectDoesNotExist:
            personal_highscore = None

        try:
            game_rating = user_object.gamerating_set.filter(game = game).first()
            if game_rating is not None:
                form = self.form_class(instance = game_rating)
                rating = game_rating.rating
            else:
                form = self.form_class(None)
                rating = 0
        except  ObjectDoesNotExist:
            form = self.form_class(None)
            rating = 0

        #game_rating = user_object.gamerating_set.filter(game = game).first()
        return render(request,'play.html',{'game':game,
                                            'is_paid':is_paid,
                                            'error_msg':error_msg,
                                            'form':form,
                                            'game_rating':game_rating,
                                            'rating':rating,
                                            'highscores':highscores,
                                            'personal_highscore':personal_highscore
                                            })


    def post(self,request,game_id):

        game = get_object_or_404(Game, pk=game_id)
        user_object = User.objects.get(id = request.user.id)

        #The cross site messaging (the LOAD/LOAD_REQUEST, SAVE and SCORE messages)
        #are processed below as they come via ajax call from play.js which is
        #part of the play game/play.html template.

        #Below input gamedata is saved to the database, provided that it exists.
        #If no game save exists, it's created for the user, otherwise the old
        #it's overwritten (so only 1 save per game!). The savedata is assumed to
        #be a string here. Json-message noting success is returned.

        #Load returns the also gamestate and messagetype in json, and an error_msg
        #message if no gamestate was found.

        #Score adds the highscore to database if received score was high enough and
        #returns the current top score via json to the calling ajax function so it
        #can be used for play.html update if necessary.

        if request.is_ajax():
            if 'messageType' in request.POST:

                if request.POST.get("messageType") == "SAVE":
                    if 'gameState' in request.POST:
                        profile = user_object.profile
                        player_gamestate = profile.gamestate_set.filter(game = game).first()
                        if player_gamestate:
                            player_gamestate.state_information = request.POST.get("gameState")
                            player_gamestate.save()
                        else:
                            player_gamestate = Gamestate(game = game, player = profile)
                            player_gamestate.state_information = request.POST.get("gameState")
                            player_gamestate.save()
                        return JsonResponse({ 'messageType':'SAVE_SUCCESS' })
                    else:
                        return JsonResponse({ 'messageType':'ERROR', 'info':'Erroneus save message!' })

                if request.POST.get('messageType') == "LOAD_REQUEST":
                    profile = user_object.profile
                    player_gamestate = profile.gamestate_set.filter(game = game).first()
                    if player_gamestate:
                        response_gamestate = player_gamestate.state_information
                        return JsonResponse({ 'messageType':'LOAD', 'gameState':response_gamestate})
                    else:
                        return JsonResponse({ 'messageType':'ERROR', 'info':'No save information found!' })

                if request.POST.get("messageType") == "SCORE":
                    if 'score' in request.POST:
                        profile = user_object.profile
                        player_highscore = profile.highscore_set.filter(game = game).first()
                        if player_highscore:
                            if (player_highscore.score < int(request.POST.get("score"))):
                                player_highscore.score = int(request.POST.get("score"))
                                player_highscore.save()
                        else:
                            player_highscore = Highscore(game = game, player = profile)
                            player_highscore.score = int(request.POST.get("score"))
                            player_highscore.save()
                        temp_current_highscore = player_highscore.score
                        return JsonResponse({ 'messageType':'SCORE_SUCCESS', 'score':temp_current_highscore })
                    else:
                        return JsonResponse({ 'messageType':'ERROR', 'info':'Erroneus score message!' })

                #Below is non-functional message type which can be used to implement achievements from
                #games (essentially just an addional class in the models which is linked to games and users)
                #It's not finished, but it can showcase that the service is somewhat modular and you
                #can add additional classes and message types to the service for additional functionality.
                if request.POST.get("messageType") == "ACHIEVEMENT":
                        return JsonResponse({ 'messageType':'ACHIEVEMENT_SUCCESS' })

        #Non-iframe/cross-site messagin related stuff is below
        error_msg = None

        try:
            game_rating = user_object.gamerating_set.filter(game = game).first()

        except ObjectDoesNotExist:
            game_rating = GameRating(game = game)
            game_rating.save()
            game_rating.add(user_object)

        form = self.form_class(request.POST,instance = game_rating)
        if form.is_valid():
            rating = form.save(commit = False)
            rating.game = game
            rating.save()

            rating.user.add(user_object)
            rating.save()

        try:
            user_games = user_object.profile.games.all()
            if user_games.filter(id=game.id).exists():
                is_paid = True
        except  ObjectDoesNotExist:
            is_paid = False
            error_msg = "you don't have access to this game"


        return render(request,'play.html',{'game':game,
                              'is_paid':is_paid,
                              'error_msg':error_msg,
                              'form':form,
                              'rating':rating.rating
                              })



@login_required(login_url="/login/")
def payment_success(request):

    pid = request.GET.get('pid')
    ref = request.GET.get('ref')
    result = request.GET.get('result')
    checksum = request.GET.get('checksum')
    token= settings.PAYMENT_SECRET_KEY
    cal_checksum = get_hashed_check_sum(pid,ref,result,token,select = 1)

    timestamp,game_id = pid.split('-')

    if(result != 'success'):
        request.session['error_msg'] = "Bad request: probably due to payment service failure, please try again"
        return redirect('storefront:game_detail',game_id = game_id)

    if(cal_checksum != checksum):
        request.session['error_msg'] = "Invalid payment data: please try again"
        return redirect('storefront:game_detail',game_id = game_id)

    try:
        game = Game.objects.get(id = int(game_id))
    except ObjectDoesNotExist:
       request.session['error_msg'] = "Server internal error: please try again"
       return redirect('storefront:game_detail',game_id = game_id)

    #TODO: game should not exist with out developer, raise error otherwise

    user = User.objects.get(id = request.user.id)
    user.profile.games.add(game) #user can now play this game
    user.save()

    payment = Payments(ref = ref,customer=user, game = game, developer = game.developer, paid_amount=game.price)
    payment.save()



    request.session['info_msg'] = "payment succeeded thank you, u can now play the game"
    return redirect('storefront:game_detail',game_id = game_id)




def payment_cancel(request):
    pid = request.GET.get('pid')
    timestamp,game_id = pid.split('-')
    return redirect('storefront:game_detail',game_id = game_id)

def payment_error(request):
    pid = request.GET.get('pid')
    timestamp,game_id = pid.split('-')
    request.session['error_msg'] = "Bad request: probably due to payment service failure, please try again"
    return redirect('storefront:game_detail',game_id = game_id)

# Generating top 5 scores for each game in scores.html page.
def scores(request):
    games = Game.objects.all();
    game_highscores = {}
    for game in games:
        highscores = Highscore.objects.filter(game = game).order_by('-score')[:5];
        for score in highscores:
            player = User.objects.get(id = score.player.id)
            score.player_nickname = player.username

        game.highscores = highscores


    context = {
        'games': games,
        'game_highscores': game_highscores
    }
    return render(request,'scores.html',context)


#Temporary functionality to enable access to our test games in the gameservice server.
#For the "real" imlementation where games would reside in some outside server, these would not be needed.
@xframe_options_exempt
def testgame1(request):
    context = {}
    return render(request,'testgame1.html',context)

@xframe_options_exempt
def snake(request):
    context = {}
    return render(request,'snake.html',context)

@xframe_options_exempt
def supersimple(request):
    context = {}
    return render(request,'supersimple.html',context)
