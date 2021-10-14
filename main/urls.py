from django.urls import path
from .views import IndexView, ShopView, CategoryView

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('shop', ShopView.as_view(), name='shop'),
    path('category/<str:cat>', CategoryView.as_view(), name='category'),
]