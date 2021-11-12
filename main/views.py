from django import forms
from django.core import paginator
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Product, Cart, Favorites, ProductReview, WebsiteReview
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import AddToCartForm, AddToFavortitesForm, ProductReviewForm, WebsiteReviewForm
from django.db.models import QuerySet, query
from django.contrib.auth.models import AnonymousUser 
from datetime import date, timedelta
from django.core.mail import send_mail
from django.http import JsonResponse
import json

class IndexView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()

        context = {
            'products':products,
            'total_no_of_products': total_no_of_products,
        }

        return render(request, 'main/index.html', context)


class ShopView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        prod = Product().categories

        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()
        
        context = {
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': prod,
            'total_no_of_products': total_no_of_products,
        }

        return render(request, 'main/shop.html', context)

class CategoryView(View):
    def get(self, request, cat, *args, **kwargs):
        products = Product.objects.filter(category=cat)

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        prod = Product().categories

        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()

        context= {
            'page_obj': page_obj,
            'paginator': paginator,
            'categories': prod,
            'total_no_of_products': total_no_of_products,
        }
        return render(request, 'main/category.html', context)        

class ProductDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        form = AddToCartForm() 

        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()

        context = {
            'product': product,
            'form': form,
            'total_no_of_products': total_no_of_products,
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

class CartView(View):
    def get(self, request, *args, **kwargs):
        cart_objects = Cart.objects.filter(user = request.user)
        total_no_of_products = cart_objects.count()

        subtotal = []
        for objects in cart_objects:
            subtotal.append(objects.sub_total)

        subtotal2 = sum(subtotal)
        delivery_fee = 0                 # Just equal to zero for now....
        total = subtotal2 + delivery_fee   
        
        context={
            'cart_objects': cart_objects,
            'total_no_of_products': total_no_of_products,
            'total': total,
            'subtotal2': subtotal2,
            'delivery_fee': delivery_fee,
        }
        return render(request, 'main/cart.html', context)


class AddToCartFromCartPage(View):
    def get(self, request, pk, *args, **kwargs):
        cart_objects = Cart.objects.filter(user = request.user)
        product = cart_objects.get(product_id = pk)

        if product.quantity > 0 or product.quantity == 0:
            product.quantity += 1
            product.sub_total = product.product.price * product.quantity
            product.save()
        return redirect('cart')

class RemoveFromCartFromCartPage(View):
    def get(self, request, pk, *args, **kwargs):
        cart_objects = Cart.objects.filter(user = request.user)
        product = cart_objects.get(product_id = pk)

        if product.quantity > 0:
            product.quantity -= 1
            product.sub_total = product.product.price * product.quantity
            product.save()
        else:
            product.delete()
        return redirect('cart')

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        cart_objects = Cart.objects.filter(user = request.user)
        total_no_of_products = cart_objects.count()

        subtotal = []
        for objects in cart_objects:
            subtotal.append(objects.sub_total)

        subtotal2 = sum(subtotal)
        delivery_fee = 0                 # Just equal to zero for now....
        total = subtotal2 + delivery_fee   
        
        form = WebsiteReviewForm()

        context={
            'total_no_of_products': total_no_of_products,
            'total': total,
            'subtotal2': subtotal2,
            'delivery_fee': delivery_fee,
            'form': form,
        }

        return render(request, 'main/checkout.html', context)

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        products = Product.objects.filter(name__icontains= query)

        prod = Product().categories

        if products:

            context = {
                'products': products,
                'categories': prod,
            }
            return render(request, 'main/search.html', context)
        else:
            messages.info(request, 'This product is not available now, please check on a later date, thank you.')
            return redirect('index')

class FavoritesView(LoginRequiredMixin,View):
    redirect_field_name = 'redirect_to'
    def post(self, request, pk, *args, **kwargs):
        form = AddToFavortitesForm(request.POST)

        if form.is_valid:
            favorites_data = form.save(commit=False)
            favorites_data.user = request.user
            favorites_data.product = Product.objects.get(id=pk)
            favorites_data.save()

        return redirect('shop')


class FavoritesPageView(View):
    def get(self, request, *args, **kwargs):
        favorites = Favorites.objects.filter(user = request.user)

        cart_objects = Cart.objects.filter(user = request.user)
        total_no_of_products = cart_objects.count()

        context = {
            'favorites': favorites,
            'total_no_of_products': total_no_of_products,
        }
        return render(request, 'main/favorites.html', context)

class WebsiteReviewView(View):
    def post(self, request, *args, **kwargs):
        form = WebsiteReviewForm(request.POST)

        if form.is_valid:
            review_data = form.save(commit=False)
            review_data.user = request.user
            review_data.save()

        messages.info(request, 'Thank you for the feedback.')

        return redirect('checkout')

class WebsiteReviewPage(View):
    def get(self, request, *args, **kwargs):
        reviews = WebsiteReview.objects.all()

        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()

        context = {
            'reviews': reviews,
            'total_no_of_products': total_no_of_products, 
        }
        return render(request, 'main/website-review.html', context)

class NewThisWeekView(View):
    startdate = date.today()
    enddate = startdate - timedelta(days=6)

    def get(self, request, *args, **kwargs):
        products_this_week = Product.objects.filter(date__range=[self.startdate, self.enddate])

        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()

        context = {
            'products_this_week': products_this_week,
            'total_no_of_products': total_no_of_products,
        }
        return render(request, 'main/new-this-week.html', context)

class ProductReviewView(View):
    def get(self, request, pk, *args, **kwargs):
        form = ProductReviewForm()

        cart_objects = Cart.objects.filter(user = request.user)
        total_no_of_products = cart_objects.count()

        context = {
            'form': form,
            'total_no_of_products': total_no_of_products,
        }
        return render(request, 'main/product-review.html', context)


    def post(self, request, pk, *args, **kwargs):
        form = ProductReviewForm(request.POST)

        if form.is_valid:
            review_data = form.save(commit=False)
            review_data.user = request.user
            review_data.product = Product.objects.get(pk=pk)
            form.save()
        return redirect('index')  # or the product page

class ProductReviewPage(View):
    def get(self, request, pk,  *args, **kwargs):
        product_reviews = ProductReview.objects.filter(product_id=pk)

        if not request.user.is_authenticated:
             total_no_of_products = 0
        else:
            cart_objects = Cart.objects.filter(user = request.user)
            total_no_of_products = cart_objects.count()
            
        if product_reviews.count() > 0:
            context = {
                'product_reviews': product_reviews,
                'total_no_of_products': total_no_of_products, 
            }
            return render(request, 'main/product-reviews-page.html', context)
        
        message = messages.info(request, 'No reviews yet, be the first to review the product.')
        context = {
            'message': message,
            'total_no_of_products': total_no_of_products, 
        }
        return render(request, 'main/product-reviews-page.html', context)
        

def newsletter(request):
    if request.method == 'POST':
        subject= 'subscription to our newsletter'
        message= 'This user would like to subcribe to our newsletter'
        from_email= request.POST['email']

        #send mail
        send_mail(
            subject, # subject
            message, # message
            from_email, # from email
            ['admin@gmail.com'], # To email


        )
        messages.info(request, 'Thank you for subscribing to our newsletter, we promise not to dissapoint.')

        return redirect('index')    

    else:    
        messages.info(request, 'There was an error, please try again later.')
        return redirect('index')   

def completeorder(request):
    user = request.user
    Cart.objects.filter(user=user).delete()
    return JsonResponse('Payment completed!', safe=False)