from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def courses_index(request):
    return HttpResponse("courses")


def courses_id(request, id):
    return HttpResponse(f"id {id}")


def courses_category(request, name):
    return HttpResponse(f"category {name}")


def courses_search(request, name):
    return HttpResponse(f"search {name}")


def courses_id_modules(request, id):
    return HttpResponse("id_modules")


def courses_id_module_id(request, id, id_module):
    return HttpResponse("id_modules")


def courses_id_module_id_lecture(request, id, id_module, id_lecture):
    return HttpResponse("courses_id_module_id_lecture")


def courses_id_module_id_test(request, id, id_module, id_test):
    return HttpResponse("courses_id_module_id_test")
