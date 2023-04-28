from django.contrib import admin
from django.urls import path, include

from profiles import views


urlpatterns = [
    path('', views.profiles_index, name="profile"),
    path('register', views.profiles_register),
    path('login', views.profiles_login, name="login"),
    path('logout', views.profiles_logout, name="logout"),
    path('courses', views.user_courses),
    path('course/<int:id_course>', views.user_course_id),
    path('add_course', views.teacher_add_courses),
    path('delete_course/<int:id_course>', views.teacher_delete_id),
    path('wishlist', views.student_wishlist)
]

