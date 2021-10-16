from django import forms
from django.core import paginator
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Product, Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import AddToCartForm
from django.db.models import QuerySet

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

class ProductDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        form = AddToCartForm() 

        context = {
            'product': product,
            'form': form
        }
        return render(request, 'main/product-details.html', context)

class AddToCartView(LoginRequiredMixin, View):
    redirect_field_name = 'redirect_to'
    def post(self, request, pk, *args, **kwargs):
        form = AddToCartForm(request.POST)
        cart_objects = Cart.objects.filter(user = request.user)
        product_in_cart = cart_objects.filter(product_id = pk).exists()
        
        if product_in_cart:
            messages.info(request, 'This product is already in your Cart')
            return redirect('product_detail', pk = pk)
        else:
            if form.is_valid():
                cart_data = form.save(commit=False)
                cart_data.user = request.user
                cart_data.product = Product.objects.get(pk=pk)
                cart_data.sub_total = cart_data.product.price * cart_data.quantity
                cart_data.save()
        return redirect('product_detail', pk=pk )