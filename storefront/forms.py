from storefront.models import GameRating
from django import forms

class GameRatingForm(forms.ModelForm):
	class Meta:
		model = GameRating
		fields = ['rating']
