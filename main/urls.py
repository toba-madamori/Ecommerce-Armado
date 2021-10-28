from django.urls import path
from .views import IndexView, ShopView, CategoryView, ProductDetailView, AddToCartView, CartView, AddToCartFromCartPage, RemoveFromCartFromCartPage, CheckoutView, SearchView, FavoritesView, FavoritesPageView, WebsiteReviewView, WebsiteReviewPage, NewThisWeekView, ProductReviewView, ProductReviewPage

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('shop', ShopView.as_view(), name='shop'),
    path('category/<str:cat>', CategoryView.as_view(), name='category'),
    path('product/detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('cart/add/<int:pk>', AddToCartView.as_view(), name='add_cart'),
    path('cart', CartView.as_view(), name='cart'),
    path('add/to/cart/<int:pk>', AddToCartFromCartPage.as_view(), name='add_to_cart'),
    path('remove/cart/<int:pk>', RemoveFromCartFromCartPage.as_view(), name='remove_cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('search', SearchView.as_view(), name='search'),
    path('favorites/<int:pk>', FavoritesView.as_view(), name='add_favorites'),
    path('favorites/list', FavoritesPageView.as_view(), name='favorites'),
    path('review', WebsiteReviewView.as_view(), name='review'),
    path('review/page', WebsiteReviewPage.as_view(), name='review_page'),
    path('new/this/week', NewThisWeekView.as_view(), name='new_this_week'),
    path('product/review/<int:pk>', ProductReviewView.as_view(), name='product_review'),
    path('product/review/page/<int:pk>', ProductReviewPage.as_view(), name='product_review_page'),
]