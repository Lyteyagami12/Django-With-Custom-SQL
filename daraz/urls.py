
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.list_jobs, name='test'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name = 'home'),
    path('home/sell/', views.sell, name='sell'),
    path('home/login/', views.user_login),
    path('home/sigunp/', views.signup),
    path('home/sell/sellsignup/', views.sellsignup),
    path('home/sell/sellsignup/saleLogin/',views.selllogin),
    path('home/sell/saleLogin/', views.selllogin),
    path('home/sell/saleLogin/saleLogin/sellsignup/', views.sellsignup),
    path('home/sell/sellsignup/saleLogin/saleLogin/sellsignup/',views.sellsignup),
    path('home/sell/sellsignup/saleLogin/saleLogin/sellsignup/saleLogin/',views.selllogin),
    path('saleLogin/',views.selllogin),
    path('saleLogin/saleLogin/sellsignup/',views.sellsignup),
    path('login/home/',views.home),

]
