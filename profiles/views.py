from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from courses.models import UserCourse, Test, Module, UserTest, Course

from profiles.models import User
from django.contrib.auth import login, authenticate, logout

from profiles.form import LoginForm, SignUpForm
from django.contrib.auth.hashers import check_password

from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def count_course_mark(user_id, course_id):
    course = Course.objects.filter(id=course_id).first()
    count_tests = 0
    total_mark = 0
    for module in course.modules.all():
        count_tests += Test.objects.filter(module_id=module.id).count()
        for test in module.tests.all():
            user_test = UserTest.objects.filter(user_id=user_id, test_id=test.id)
            for user_test_module in user_test:
                total_mark += user_test_module.grade
    if not count_tests:
        total_mark = 0
    else:
        total_mark = total_mark / count_tests
    return total_mark


class Rating:
    def __init__(self, user, total_mark):
        self.user = user
        self.total_mark = total_mark


def rating_course(course_id):
    total_marks = {}
    users = []
    course_users = UserCourse.objects.filter(course_id=course_id)
    for course_user in course_users:
        total_marks[course_user.user.id] = count_course_mark(course_user.user.id, course_id)
        # print(course_user.user.id)
    total_marks = sorted(total_marks.items(), key=lambda x: x[1], reverse=True)
    for key, value in total_marks:
        # users.append(User.objects.get(id=key))
        users.append(Rating(User.objects.get(id=key), value))
    # print(users)
    return users


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


@login_required(login_url='login')
def profiles_index(request):
    user = request.user
    if user.is_authenticated:
        courses = UserCourse.objects.filter(user_id=user.id)
        count = 0
        result = 0
        courses_pass = []
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
    if request.method == 'POST':
        print(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        errors = form.errors.as_data()
        return render(request, 'sign_up.html', {'form': form, 'errors': errors, 'user': request.user})

    else:
        form = SignUpForm()
        return render(request, 'sign_up.html', {'form': form, 'user': request.user})


# @login_required
def profiles_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("valid")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            form.errors.clear()
            try:
                user = User.objects.filter(email=email)
                if user:
                    user = user[0]
                    if check_password(password, user.password) or password == user.password:
                        login(request, user)
                        print("good")
                        return redirect('profile')
                    else:
                        form.add_error('password', 'Неправильно введений пароль')
                        raise User.DoesNotExist
                else:
                    form.add_error('email', 'Не існує користувача з такою поштою')
                    raise User.DoesNotExist
            except User.DoesNotExist:

                return render(request, 'login.html', {'form': form, 'user': request.user})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form, 'user': request.user})


def profiles_logout(request):
    logout(request)
    return redirect('main')


def student_check(user):
    if user.is_authenticated:
        return user.role == "student" or user.role == "teacher" or user.role == "admin"
    else:
        return False


@login_required(login_url='login')
@user_passes_test(student_check)
def user_courses(request):
    from courses.views import enroll_course
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            error = enroll_course(request)
            if error:
                return render(request, 'error.html', context={'error': error})
        else:
            return redirect('login')
    if user.is_authenticated:
        courses = UserCourse.objects.filter(user_id=user.id)
        courses_pass = []
        wishlist = get_wishlist(request)
        for course in courses:
            courses_pass.append(count_course_pass(user.id, course.course_id))
        return render(request, 'usercourses.html',
                      context={"courses": zip(courses, courses_pass), 'user': request.user, 'wishlist': wishlist})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})
    # return HttpResponse("teacher_courses")


@login_required(login_url='login')
@user_passes_test(student_check)
def user_course_id(request, id_course):
    user = request.user
    if user.is_authenticated and Course.objects.filter(id=id_course):
        print(user.id, id_course)
        count = count_course_pass(user.id, id_course)
        mark = count_course_mark(user.id, id_course)

        return HttpResponse(f"Результат прогресу курсу: {count}%, оцінка за курс: {mark}%")


def student_wishlist(request):
    from courses.views import enroll_course
    courses = []
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            error = enroll_course(request)
            if error:
                return render(request, 'error.html', context={'error': error})
        else:
            return redirect('login')
    if 'Wishlist_user' in request.COOKIES:
        cookie = request.COOKIES['Wishlist_user']
        wishlist = cookie.split(',')
        wishlist = list(map(int, wishlist))
        for i in wishlist:
            course = Course.objects.filter(id=i)
            if course:
                courses.append(course[0])
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
    wishlist = get_wishlist(request)
    response = render(request, 'wishlist.html',
                      context={"courses": show_course_enroll, 'user': request.user, 'wishlist': wishlist})
    return response


def change_wishlist(request):
    previous_page = request.META.get('HTTP_REFERER')
    response = HttpResponseRedirect(previous_page)
    if 'Wishlist_user' in request.COOKIES:
        cookie = request.COOKIES['Wishlist_user']
        wishlist = cookie.split(',')
        wishlist = list(map(int, wishlist))
    else:
        wishlist = []
    if int(request.POST['id']) not in wishlist:
        wishlist.append(int(request.POST['id']))
    else:

        if len(wishlist) != 1:
            wishlist.remove(int(request.POST['id']))
        else:
            print('346')
            response.delete_cookie('Wishlist_user')
            return response

    serialized_list = ','.join(map(str, wishlist))


    response.set_cookie('Wishlist_user', serialized_list)
    return response


def get_wishlist(request):
    if 'Wishlist_user' in request.COOKIES:
        cookie = request.COOKIES['Wishlist_user']
        wishlist = cookie.split(',')
        wishlist = list(map(int, wishlist))
    else:
        wishlist = []
    return wishlist
