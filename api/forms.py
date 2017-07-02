from django import forms
from storefront.models import API_AUTH

class token_regenerate_form(forms.ModelForm):
    class Meta:
        model = API_AUTH
        fields = ['sid','skey']
