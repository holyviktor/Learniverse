from django.http import HttpResponse
from django.shortcuts import render
from courses.models import Category, Course, Module, Lection, Test, Question, Answer
# Create your views here.
def main_index(request):
    courses = Course.objects.filter()
    return render(request, 'index.html', context={"courses": courses})


def main_about(request):
    return HttpResponse("about")
