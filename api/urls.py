from django.conf.urls import include, url
from django.contrib import admin
from . import views
from gameshop import settings
from django.contrib.staticfiles.urls import static
app_name = 'api'

urlpatterns = [
    url(r'^$', views.Index),
    url(r'^v1/games/(?P<game_id>[0-9]+)/', views.Games),
    url(r'^v1/games/', views.Games),
    url(r'^v1/sales/', views.sales),
    url(r'^v1/scores/(?P<game_id>[0-9]+)/', views.scores),
    url(r'^v1/scores/', views.scores),
    url(r'^regenerate_token/', views.regenerate_token,name='regenerate_token'),
]
