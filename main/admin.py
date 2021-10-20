from django.contrib import admin
from .models import Cart, Product, User, Favorites

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favorites)