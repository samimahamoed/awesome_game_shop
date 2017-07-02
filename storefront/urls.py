from django.conf.urls import url
from . import views
app_name = 'storefront'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^games/detail/(?P<game_id>[0-9]+)/', views.game_detail, name='game_detail'),
    url(r'^games/play/(?P<game_id>[0-9]+)/', views.Play.as_view(), name='play'),
    url(r'^games/play/', views.Play.as_view(), name='play'),
    url(r'^games/payment/success/', views.payment_success, name='payment_success'),
    url(r'^games/payment/cancel/', views.payment_cancel, name='payment_cancel'),
    url(r'^games/payment/error/', views.payment_error, name='payment_error'),
    url(r'^games/search', views.search_games, name='search_games'),
    url(r'^games', views.games, name='games'),
    url(r'^scores', views.scores, name='scores'),
    url(r'^games/highscore/(?P<game_id>[0-9]+)', views.ajax_highscores),
    #Links temporarily to the game service
    url(r'^games/testgame1/', views.testgame1, name='testgame1'),
    url(r'^games/testgame2/', views.testgame1, name='testgame1'),
    url(r'^games/snake/', views.snake, name='snake'),
    url(r'^games/supersimple/', views.supersimple, name='supersimple'),
]
    #Game html/js files are hosted temporarily in the gameservice server for testing showcasing purposes.
    #Therefore there is functionality in urls.py, views.py and with templates to enable these. In the "real" case,
    #this functioality is taken out and the game model url links to some outside webpage instead.
