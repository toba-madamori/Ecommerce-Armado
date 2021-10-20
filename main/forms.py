from django import forms
from django.forms import ModelForm, fields, models
from .models import Cart, Favorites

class AddToCartForm(models.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity',]
    
class AddToFavortitesForm(models.ModelForm):
    class Meta:
        model = Favorites
        fields = []