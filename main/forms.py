from django import forms
from django.forms import ModelForm, fields, models
from .models import Cart, Favorites, ProductReview, WebsiteReview

class AddToCartForm(models.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity',]
    
class AddToFavortitesForm(models.ModelForm):
    class Meta:
        model = Favorites
        fields = []

class WebsiteReviewForm(models.ModelForm):
    class Meta:
        model = WebsiteReview
        fields = ['review']

        widgets = {
            'review': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Did you like our e-shop?'}), 
        }

class ProductReviewForm(models.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review']

        widgets = {
            'review': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your thoughts on the product'}), 
        }