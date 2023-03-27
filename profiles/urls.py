from django.contrib import admin
from django.urls import path, include

from profiles import views

# from tours.views import tours
# from cart.views import cart

urlpatterns = [
    path('', views.profiles_index),
    path('register', views.profiles_register),
    path('login', views.profiles_login),
]

urlpatterns = [
    path('profile', views.teacher_profile),
    path('courses', views.teacher_courses),
    path('course/<int:id_course>', views.teacher_course_id),
    path('add_course', views.teacher_add_courses),
    path('delete_course/<int:id_course>', views.teacher_delete_id),
]


urlpatterns = [
    path('profile', views.student_profiles),
    path('wishlist', views.student_wishlist),
    path('courses', views.student_courses),
]
