from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from courses.models import UserCourse, Test, Module, UserTest, Course
from profiles.models import User
from django.contrib.auth import login, authenticate, logout

from profiles.form import LoginForm


def count_course_pass(user_id, course_id):
    modules = Module.objects.filter(course_id=course_id)
    test_course_count = 0
    user_tests_count = 0
    for module in modules:
        tests = Test.objects.filter(module_id=module.id)
        for test in tests:
            test_course_count += 1
            user_test = UserTest.objects.filter(user_id=user_id, test_id=test.id)
            if user_test:
                user_tests_count += 1
    if not test_course_count:
        return 0
    return user_tests_count / test_course_count * 100


# @login_required
# Create your views here.
def profiles_index(request):
    # print("here i am")
    # user_id = request.session.get("user_id")
    # print(user_id)
    # user_id = 1

    user = request.user
    print(user)
    # id = request.session.get("user_id")
    # user = User.objects.get(id=id)
    if user.is_authenticated:
        courses = UserCourse.objects.filter(user_id=user.id)
        count = 0
        result = 0

        courses_pass = []
        print(len(courses))
        if len(courses) != 0:
            for course in courses:
                courses_pass.append(count_course_pass(user.id, course.course_id))
            count = len(courses)
            result = round(sum(courses_pass) / count, 2)
        return render(request, 'user.html',
                      context={"user": user, "count": count, "result": result, "courses": zip(courses, courses_pass)})
    else:
        return redirect('login')


def profiles_register(request):
    return HttpResponse('register')


# @login_required
def profiles_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email, password=password)
                login(request, user)
                return redirect('profile')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def profiles_logout(request):
    logout(request)

    return redirect('main')


def student_check(user):
    print(user)
    if user.is_authenticated:
        return user.role == "student"
    else:
        return False


# @login_required(login_url='login')
# @user_passes_test(student_check)
def user_courses(request):
    user = request.user
    # user_id = request.session.get("user_id")
    # print(user_id)
    # user_id = 1
    if user.is_authenticated:
        # user = User.objects.get(id=1)
        courses = UserCourse.objects.filter(user_id=user.id)
        courses_pass = []
        print(courses)
        for course in courses:
            # print(course.id)
            # print(courses[course])
            print(user.id)
            print(course.course_id)
            courses_pass.append(count_course_pass(user.id, course.course_id))
        print(courses_pass)
        # print(len(courses))

        return render(request, 'usercourses.html', context={"courses": zip(courses, courses_pass)})
    return HttpResponse("teacher_courses")


def user_course_id(request, id_course):
    user = request.user
    # user_id = request.session.get('user_id')
    if user.is_authenticated and Course.objects.filter(id=id_course):
        print(user.id, id_course)
        count = count_course_pass(user.id, id_course)
        return HttpResponse(f"Результат проходження курсу: {count}%")


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")


def teacher_delete_id(request, id):
    return HttpResponse("teacher_delete_id")


def student_wishlist(request):
    wishlist = request.COOKIES['wishlist']
    courses = []
    for i in wishlist:
        courses.append(Course.objects.get(id=i))

    response = render(request, 'usercourses.html', context={"courses": courses})
    return response


def add_course_to_wishlist(request, id):
    previous_page = request.META.get('HTTP_REFERER')
    wishlist = request.COOKIES['wishlist']
    wishlist.append(id)
    response = HttpResponseRedirect(previous_page)
    response.set_cookie('wishlist', wishlist)

    return response


def del_course_to_wishlist(request, id):
    previous_page = request.META.get('HTTP_REFERER')
    wishlist = request.COOKIES['wishlist']
    wishlist.remove(id)
    response = HttpResponseRedirect(previous_page)
    response.set_cookie('wishlist', wishlist)

    return response
