from django.urls import path

from . import views

urlpatterns = [
    path('', views.courses_index, name="courses"),
    path('<int:id>', views.courses_id, name="course"),  #
    path('search/<str:name>', views.courses_search),
    path('category/<str:name>', views.courses_category),  #
    path('<int:id>/modules', views.course_modules, name="modules"),
    path('<int:id>/module/<int:id_module>', views.courses_id_module_id, name="module"),  #
    path('<int:id>/module/<int:id_module>/lecture/<int:id_lecture>', views.courses_id_module_id_lecture,
         name="lecture"),
    path('<int:id>/module/<int:id_module>/test/<int:id_test>', views.courses_id_module_id_test, name="test"),  #
    path('video', views.video),
    path('<int:id>/certificate', views.certificate, name='certificate'),
    path('<int:id>/generate_certificate', views.generate_certificate, name='generate_certificate'),
    path('<int:id>/send_certificate', views.send_certificate, name='send_certificate'),
    # path('<int:id>/download-certificate/', views.download_certificate, name='download_certificate'),
]
