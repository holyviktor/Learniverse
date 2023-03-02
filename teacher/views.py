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