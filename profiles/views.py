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
    total_mark = total_mark / count_tests
    return total_mark


def rating_course(course_id):
    total_marks = {}
    users = []
    course_users = UserCourse.objects.filter(course_id=course_id)
    for course_user in course_users:
        total_marks[course_user.user.id] = count_course_mark(course_user.user.id, course_id)
        print(course_user.user.id)
    total_marks = sorted(total_marks.items(), key=lambda x: x[1], reverse=True)
    for key, value in total_marks:
        users.append(User.objects.get(id=key))
    print(users)
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
    # print("here i am")
    # user_id = request.session.get("user_id")
    # print(user_id)
    # user_id = 1

    user = request.user

    # id = request.session.get("user_id")
    # user = User.objects.get(id=id)
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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('profile')
                else:
                    raise User.DoesNotExist
            except User.DoesNotExist:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'user': request.user})


def profiles_logout(request):
    logout(request)

    return redirect('main')


def student_check(user):
    if user.is_authenticated:
        return user.role == "student"
    else:
        return False


@login_required(login_url='login')
@user_passes_test(student_check)
def user_courses(request):
    user = request.user
    if user.is_authenticated:

        courses = UserCourse.objects.filter(user_id=user.id)
        courses_pass = []

        for course in courses:
            courses_pass.append(count_course_pass(user.id, course.course_id))
        return render(request, 'usercourses.html',
                      context={"courses": zip(courses, courses_pass), 'user': request.user})
    return HttpResponse("teacher_courses")


@login_required(login_url='login')
@user_passes_test(student_check)
def user_course_id(request, id_course):
    user = request.user

    if user.is_authenticated and Course.objects.filter(id=id_course):
        print(user.id, id_course)
        count = count_course_pass(user.id, id_course)
        mark = count_course_mark(user.id, id_course)
        return HttpResponse(f"Результат прогресу курсу: {count}%, оцінка за курс: {mark}%")


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")


def teacher_delete_id(request):
    return HttpResponse("teacher_delete_id")


def student_wishlist(request):
    courses = []
    if 'Wishlist_user' in request.COOKIES:
        cookie = request.COOKIES['Wishlist_user']
        wishlist = cookie.split(',')
        wishlist = list(map(int, wishlist))
        for i in wishlist:
            courses.append(Course.objects.get(id=i))
    response = render(request, 'wishlist.html', context={"courses": courses, 'user': request.user})
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


def generate_certificate(request):
    participant_name = "John Doe"  # Замініть на реальне ім'я учасника

    # Генерація сертифіката у форматі PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica", 24)
    p.drawString(100, 700, "certificate")
    p.setFont("Helvetica", 16)
    p.drawString(100, 650, "Цей сертифікат видається")
    p.setFont("Helvetica", 20)
    p.drawString(100, 600, "за успішне проходження курсу Django")
    p.setFont("Helvetica", 24)
    p.drawString(100, 500, participant_name)

    p.showPage()
    p.save()

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    return response