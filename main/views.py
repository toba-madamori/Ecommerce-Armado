from django.shortcuts import render
from django.views import View
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            'products':products
        }

        return render(request, 'main/index.html', context)

