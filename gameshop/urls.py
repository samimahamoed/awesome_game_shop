"""gameshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from . import settings
from django.contrib.staticfiles.urls import static




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^social_callback/',views.social_callback,name = "social_callback"),
    url(r'^login/', views.LoginFormView.as_view(),name='login'),
    url(r'^logout/', views.logout,name='logout'),
    url(r'^email/validate/resend', views.resend_validation_email,name='resend_vemail'),
    url(r'^email/validate', views.email_validator,name='validate'),
    url(r'^register/', views.RegistrationFormView.as_view(),name='register'),
    url(r'^profile/', views.ProfileView.as_view(),name='profile'),
    url(r'^profile_img_upload/', views.image_upload,name='profile_img_upload'),
    url(r'^storefront/', include('storefront.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^', include('storefront.urls')),
    url(r'^accounts/',include('allauth.urls')),
    url(r'^addgame/', views.GameFormView.as_view(),name='addgame'),
    url(r'^deletegame/(?P<game_id>[0-9]+)/', views.delete_game,name='deletegame'),
    url(r'^editgame/(?P<game_id>[0-9]+)/', views.GameFormView.as_view(),name='editgame')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
