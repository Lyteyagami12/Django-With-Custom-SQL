
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.products),
    path('sell/',views.sell),
    path('sell/sellsignup/', views.sellsignup),
    path('sell/saleLogin/', views.selllogin),
    path('info/',views.list_jobs, name='test'),
    path('home/signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/', views.products, name = 'home'),
    # path('sell/',views.sell),
    path('home/logout/', views.user_logout, name='logout'),
    path('home/sell/', views.sell, name='sell'),
    path('home/login/', views.user_login),
    path('home/sigunp/', views.signup),
    path('home/sell/sellsignup/', views.sellsignup),
    path('home/sell/sellsignup/saleLogin/', views.selllogin),
    path('home/sell/saleLogin/', views.selllogin),
    path('home/sell/saleLogin/saleLogin/sellsignup/', views.sellsignup),
    path('home/sell/sellsignup/saleLogin/saleLogin/sellsignup/',views.sellsignup),
    path('home/sell/sellsignup/saleLogin/saleLogin/sellsignup/saleLogin/',views.selllogin),
    path('saleLogin/',views.selllogin),
    path('saleLogin/saleLogin/sellsignup/',views.sellsignup),
    path('login/home/',views.products),
    path('login/profile/', views.profile),
    path('saleproduct/', views.sale),
    path('home/login/home/',views.user_login),
    path('home/profile/',views.profile),
    path('home/order/',views.order, name = 'order'),
    path('home/cart/',views.cart),
    path('saleLogout/',views.saleLogout),
    path('home/pay/',views.check),
    path('home/shipment/',views.shipment),


]
