import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from courses.models import Course, UserCourse
from courses.views import courses_id
from profiles.models import User

from django.core.serializers import serialize


# Create your views here.
def profiles_index(request):
    user = User.objects.get(id=1)
    if user:
        return render(request, 'user.html', context={"user": user})
    return HttpResponse("profile")


def profiles_register(request):
    return HttpResponse('register')


def profiles_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = User.objects.get(email=login)
        if user.password != password:
            return HttpResponse("login")
        else:
            request.session['user'] = serialize("json", [user,])
            return redirect('profile')
# Create your views here.


def profiles_logout(request):
    request.session.delete('user')
    return redirect('main')


def user_courses(request):
    user = User.objects.get(id=1)
    if user:
        courses = UserCourse.objects.filter(user=user)
        print(len(courses))
        return render(request, 'usercourses.html', context={"courses": courses})
    return HttpResponse("teacher_courses")


def user_course_id(request, id):
    return courses_id(request,id)


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")


def teacher_delete_id(request, id):
    return HttpResponse("teacher_delete_id")


def student_wishlist(request):
    return HttpResponse("wishlist")

