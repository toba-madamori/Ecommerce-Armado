from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Product(models.Model):
    Category_choices = [
    ('chairs', 'chairs'),
    ('beds', 'beds'),
    ('tables', 'tables'),
    ('home_deco', 'home_deco'),
    ('dressings', 'dressings')
]
    name = models.CharField(max_length=100)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(upload_to ='products/')
    category = models.CharField(choices=Category_choices, max_length=50)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return self.name

    def categories(self):
        cat = self.Category_choices
        cat2 = []
        for choices in cat:
            cat2.append(choices[-1])
        return  cat2   

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  
    sub_total = models.IntegerField(blank=True, null=True)  
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name


class WebsiteReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name