
from django.contrib import admin
from django.urls import path, include
from . import views
from .checkout import checkout
from .LoginAndLogout import loginOrSignup
from .Sales import sale


urlpatterns = [
    path('',views.Index.as_view(), name = 'homepage'),
    path('sell/',views.sell),
    path('sell/sellsignup/', sale.sellsignup),
    path('sell/saleLogin/', sale.selllogin),
    path('info/',views.list_jobs, name='test'),
    path('home/signup/', loginOrSignup.signup, name='signup'),
    path('login/', loginOrSignup.user_login, name='login'),
    path('home/', views.products, name = 'home'),
    # path('sell/',views.sell),
    path('home/logout/', loginOrSignup.user_logout, name='logout'),
    path('home/sell/', views.sell, name='sell'),
    path('home/login/', loginOrSignup.user_login),
    path('home/sigunp/', loginOrSignup.signup),
    path('home/sell/sellsignup/', sale.sellsignup),
    path('home/sell/sellsignup/saleLogin/', sale.selllogin),
    path('home/sell/saleLogin/', sale.selllogin),
    # path('home/sell/saleLogin/saleLogin/sellsignup/', views.sellsignup),
    # path('home/sell/sellsignup/saleLogin/saleLogin/sellsignup/',views.sellsignup),
    # path('home/sell/sellsignup/saleLogin/saleLogin/sellsignup/saleLogin/',views.selllogin),
    path('saleLogin/',sale.selllogin),
    # path('saleLogin/saleLogin/sellsignup/',sale.sellsignup),
    path('login/home/',views.products),
    path('login/profile/', views.profile),
    path('saleproduct/', sale.sale),
    # path('home/login/home/',loginOrSignup.user_login, name='login'),
    path('home/profile/',views.profile),
    # path('home/order/',views.order, name = 'order'),
    path('home/cart/',views.cart,name = 'cart'),
    path('saleLogout/',sale.saleLogout),
    path('home/pay/',checkout.check, name= 'checkout'),
    path('home/shipment/',views.shipment),
    path('home/profile/accountsettings/',views.accountsettings),



]
