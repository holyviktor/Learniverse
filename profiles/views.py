from django.http import HttpResponse
from django.shortcuts import render, redirect

from courses.models import  UserCourse
from courses.views import courses_id
from profiles.models import User

from profiles.form import LoginForm


# Create your views here.
def profiles_index(request):
    try:
        id = request.session.get("user_id")
        user = User.objects.get(id=id)
        if user:
            return render(request, 'user.html', context={"user": user})
    except User.DoesNotExist:
        return HttpResponse("profile")


def profiles_register(request):
    return HttpResponse('register')


def profiles_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                print(user.name)
                return redirect('profile')
            except User.DoesNotExist:
                print("bad")
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def profiles_logout(request):
    del request.session['user_id']
    return redirect('main')


def user_courses(request):
    user = User.objects.get(id=1)
    if user:
        courses = UserCourse.objects.filter(user=user)
        print(len(courses))
        return render(request, 'usercourses.html', context={"courses": courses})
    return HttpResponse("teacher_courses")


def user_course_id(request, id):
    return courses_id(request, id)


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")  


def teacher_delete_id(request, id):
    return HttpResponse("teacher_delete_id")


def student_wishlist(request):
    return HttpResponse("wishlist")

