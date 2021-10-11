from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self) -> str:
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product