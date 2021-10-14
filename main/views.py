from django.core import paginator
from django.shortcuts import render
from django.views import View
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        context = {
            'products':products,
        }

        return render(request, 'main/index.html', context)


class ShopView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        prod = Product().categories
        
        context = {
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': prod,
        }

        return render(request, 'main/shop.html', context)

class CategoryView(View):
    def get(self, request, cat, *args, **kwargs):
        products = Product.objects.filter(category=cat)

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        prod = Product().categories

        context= {
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': prod,
        }
        return render(request, 'main/category.html', context)        
