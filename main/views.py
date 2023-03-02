from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def main_index(request):
    return HttpResponse("main")


def main_about(request):
    return HttpResponse("about")
