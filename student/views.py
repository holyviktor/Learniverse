from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def student_profiles(request):
    return HttpResponse("student_profile")


def student_wishlist(request):
    return HttpResponse("wishlist")


def student_courses(request):
    return HttpResponse("profile courses")

