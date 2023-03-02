from django.contrib import admin
from django.urls import path, include

from profiles import views

# from tours.views import tours
# from cart.views import cart

urlpatterns = [
    path('', views.profiles_index),
    path('register', views.profiles_register),
    path('login', views.profiles_login),
    path('wishlist', views.profiles_wishlist),
    path('courses', views.profiles_courses),
]
