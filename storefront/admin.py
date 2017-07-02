from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Game,Profile, Developers,API_AUTH

# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class DevelopersInline(admin.StackedInline):
    model = Developers
    can_delete = False
    verbose_name_plural = 'developers'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,DevelopersInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(API_AUTH)
#admin.site.register(Developers)

#Listing games in admin sites: show names and description
class GameAdmin(admin.ModelAdmin):
	list_display = ('name','description')

admin.site.register(Game, GameAdmin)
