from django.http import HttpResponse
from django.shortcuts import render
from courses.models import Category, Course, User


# Create your views here.

def main_index(request):
    courses = Course.objects.filter()
    return render(request, 'index.html', context={"courses": courses, 'user': request.user})


def main_about(request):
    return render(request, 'about.html', context={'user': request.user})
