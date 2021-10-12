from django.urls import path
from .views import IndexView, ShopView

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('shop', ShopView.as_view(), name='shop'),
]