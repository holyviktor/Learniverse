from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def profiles_index(request):
    return HttpResponse("profile")


def profiles_register(request):
    return HttpResponse("profile register")


def profiles_login(request):
    return HttpResponse("login")



from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def teacher_profile(request):
    return HttpResponse("teacher_profile")


def teacher_courses(request):
    return HttpResponse("teacher_courses")


def teacher_course_id(request, id):
    return HttpResponse("teacher_course_id")


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")


def teacher_delete_id(request, id):
    return HttpResponse("teacher_delete_id")




def student_profiles(request):
    return HttpResponse("student_profile")


def student_wishlist(request):
    return HttpResponse("wishlist")


def student_courses(request):
    return HttpResponse("profile courses")