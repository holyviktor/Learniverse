from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_index, name="main"),
    path('about', views.main_about),
]
