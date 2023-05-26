from django.http import HttpResponse
from django.shortcuts import render, redirect
from courses.models import Category, Course, User, UserCourse
from courses.views import enroll_course


# Create your views here.

def main_index(request):
    courses = Course.objects.filter()
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            enroll_course(request)
        else:
            return redirect('login')
    show_course_enroll = {}
    for course in courses:
        if user.is_authenticated:
            user_course = UserCourse.objects.filter(user_id=user.id, course_id=course.id)
            if user_course:
                show_course_enroll[course] = False
            else:
                show_course_enroll[course] = True
        else:
            show_course_enroll[course] = True
    return render(request, 'index.html', context={"courses": show_course_enroll, 'user': request.user })


def main_about(request):
    return render(request, 'about.html', context={'user': request.user})
