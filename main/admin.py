from django.contrib import admin
from .models import Cart, Product, User, Favorites, WebsiteReview

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favorites)
admin.site.register(WebsiteReview)
