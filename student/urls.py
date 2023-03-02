from django.contrib import admin
from django.urls import path, include

from student import views

# from tours.views import tours
# from cart.views import cart

urlpatterns = [
    path('profile', views.student_profiles),
    path('wishlist', views.student_wishlist),
    path('courses', views.student_courses),
]
