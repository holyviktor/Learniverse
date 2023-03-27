from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def profiles_index(request):
    return HttpResponse("profile")


def profiles_register(request):
    return HttpResponse("profile register")


def profiles_login(request):
    return HttpResponse("login")


# Create your views here.


def user_courses(request):
    return HttpResponse("teacher_courses")


def user_course_id(request, id):
    return HttpResponse("teacher_course_id")


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")


def teacher_delete_id(request, id):
    return HttpResponse("teacher_delete_id")


def student_wishlist(request):
    return HttpResponse("wishlist")

