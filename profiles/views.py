from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def profiles_index(request):
    return HttpResponse("profile")


def profiles_register(request):
    return HttpResponse("profile register")


def profiles_login(request):
    return HttpResponse("login")


