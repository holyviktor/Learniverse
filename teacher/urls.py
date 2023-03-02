from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.teacher_profile),
    path('courses', views.teacher_courses),
    path('course/<int:id_course>', views.teacher_course_id),
    path('add_course', views.teacher_add_courses),
    path('delete_course/<int:id_course>', views.teacher_delete_id),
]
