from django.contrib.auth.models import User
from storefront.models import Profile
from storefront.models import Game
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget=forms.PasswordInput)



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','email', 'username','password']

class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'username','first_name','last_name','email']

class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img_path']




class GameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = ['name','description','url','image','price']
