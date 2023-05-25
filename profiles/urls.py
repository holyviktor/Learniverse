from django.contrib import admin
from django.urls import path, include

from profiles import views

urlpatterns = [
    path('', views.profiles_index, name="profile"),
    path('register', views.profiles_register, name="sign_up"),
    path('login', views.profiles_login, name="login"),
    path('logout', views.profiles_logout, name="logout"),
    path('courses', views.user_courses, name="profile_courses"),
    path('course/<int:id_course>', views.user_course_id, name="user_course"),
    path('add_course', views.teacher_add_courses),
    path('delete_course/<int:id_course>', views.teacher_delete_id),
    path('change_wish_list', views.change_wishlist, name="like"),
    # path('delete_course_to_wish_list', views.del_course_to_wishlist, name="dislike"),
    path('wishlist', views.student_wishlist, name='wishlist')

]
