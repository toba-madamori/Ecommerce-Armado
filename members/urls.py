from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserRegisterView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', UserRegisterView.as_view(), name= 'register'),
    path('login', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]