
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.list_jobs, name='test'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name = 'home'),
    path('sell/',views.sell, name = 'sell'),
]