from django.urls import path

from . import views

urlpatterns = [
    path('', views.courses_index),
    path('<int:id>', views.courses_id),
    path('search/<str:name>', views.courses_search),
    path('category/<str:name>', views.courses_category),
    path('<int:id>/modules', views.courses_id_modules),
    path('<int:id>/module/<int:id_module>', views.courses_id_module_id),
    path('<int:id>/module/<int:id_module>/lecture/<int:id_lecture>', views.courses_id_module_id_lecture),
    path('<int:id>/module/<int:id_module>/test/<int:id_test>', views.courses_id_module_id_test),
]
