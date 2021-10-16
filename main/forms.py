from django import forms
from django.forms import ModelForm, fields, models
from .models import Cart 

class AddToCartForm(models.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity',]
    
    