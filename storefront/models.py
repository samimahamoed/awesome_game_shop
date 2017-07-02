from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

from django.core.validators import MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

#Note that for the basic "user class", we used django user
#authentication functionality and the built-in basic django user
#model as a base.

#NOTE: You can find more comments about the views-template communication and
#the cross site messaging between service and the game(iframe) in the comments
#in play.js

# This can go to other file if we have similar purpos
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

def profile_img_location(instance,filename):
    filebase,extension = filename.split('.')
    return "%s/%s.%s" %('profile',instance.user.username,extension)
    #return 'profile/'.join(instance.user.username,filename)

#The developer class can add games to the system and basically every user
#can be one without any special permission, as long as he has the normal
#credentials.
class Developers(models.Model):
    user = models.OneToOneField(User)
    active =models.BooleanField(default=False)
    starting_date = models.DateTimeField(blank=False, default=datetime.datetime.now)


class API_AUTH(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,)
    sid  = models.CharField(max_length=512,unique=True)
    skey = models.CharField(max_length=512,unique=True)



#Game model contains the required information to link them to the game developer, contains
#the pricing and also fields for accessing game image for storefront display and for
#the actual game url where it can be accessed.

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512,unique=True)
    description = models.TextField(default='',blank=True)
    image = models.ImageField(null=True,upload_to="image_uploads"
                                ,blank=True,default = 'image_uploads/placeholder.png' )
    url = models.URLField(unique=True)
    developer = models.ForeignKey(Developers, on_delete=models.CASCADE)
    price = models.FloatField(default=0, validators = [MinValueValidator(0.0)])
    publication_date = models.DateField(blank=False, default=datetime.date.today)

class GameRating(models.Model):
    game   = models.ForeignKey(Game, on_delete=models.CASCADE)
    user   = models.ManyToManyField(User)
    rating = models.IntegerField(default=1, null=False)

#Profile class is an extension of the django user class, that has more
#non-authentication related stuff such as link to the possible profile picture
#and a games list of the users owned games.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_img_path = models.ImageField(upload_to=profile_img_location,
                        storage=OverwriteStorage(),
                        blank=False,
                        default='profile/placeholder.png',
                        height_field= "height",
                        width_field = "width")
    height  = models.IntegerField(default=100)
    width   = models.IntegerField(default=100)
    games   = models.ManyToManyField(Game)
    email_vaidated  =  models.BooleanField(default=False)


#Below couple of listener functions that create profile automatically
#when a user is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Payments(models.Model):
    ref    = models.IntegerField(unique=True, null=False)
    customer   = models.ForeignKey(User,on_delete=models.CASCADE)
    game   = models.ForeignKey(Game,on_delete=models.CASCADE)
    developer = models.ForeignKey(Developers,on_delete=models.CASCADE)
    paid_amount = models.FloatField(default=0)
    date = models.DateField(blank=False, default=datetime.date.today)


#Each player can have 1 highscore for each game and these are stored with these
#help of this class. The player and game fields link the highscore to the
#relevant entities so it can be accessed easily.
class Highscore(models.Model):
    player = models.ForeignKey(Profile)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    player_nickname = models.CharField(max_length=15)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    modified = models.DateTimeField(auto_now=True)

#This class offers possibility to make achievements for a game, where
#they could be presented on the play game page if needed. The messaging
#and our test games don't implement/utilize these, though, but this
#can showcase that the service has potential for easy addition of extra
#features
class Achievement(models.Model):
    player = models.ForeignKey(Profile,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    description = models.CharField(max_length=512)
    created = models.DateTimeField(auto_now_add=True,auto_now=False)
    image = models.ImageField(null=True,upload_to="image_uploads")

#This class could be used for more complex game settings that need to be stored
#If additional fields are to be added. This was not utilized/implemented with
#the messaging and our test games, though. Another possible extra feature, though.
class Gamesettings(models.Model):
    player = models.ForeignKey(Profile,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()

#Saved game information is stored with this class - the state information
#is essentially json data that is in string form. It's linked to both user
#and game to identify the proper relations. Only 1 save game state per game
#per user is assumed.
class Gamestate(models.Model):
    player = models.ForeignKey(Profile,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    state_information = models.CharField(max_length=512,blank=True)
    score = models.IntegerField(default=0)
