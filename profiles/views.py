from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect

from courses.models import UserCourse, Test, Module, UserTest, Course
from profiles.models import User

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
    print("here i am")
    try:
        id = request.session.get("user_id")
        user = User.objects.get(id=id)
        if user:
            print("hereeeeeeeeee")
            return render(request, 'user.html', context={"user": user})
    except User.DoesNotExist:
        return HttpResponse("profile")


def profiles_register(request):
    return HttpResponse('register')


def profiles_login(request):
    print(request.session.get('user_id'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email, password=password)
                request.session['user_id'] = user.id
                print(request.session['user_id'])
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


def student_check(user):
    print(user)
    if user:
        return user.role == "student"
    else:
        return False


# @login_required(login_url='login')
# @user_passes_test(student_check)
def user_courses(request):
    user_id = request.session.get("user_id")
    print(user_id)
    # user_id = 1
    if user_id:
        user = User.objects.get(id=1)
        courses = UserCourse.objects.filter(user_id=user_id)
        courses_pass = []
        print(courses)
        for course in courses:
            # print(course.id)
            # print(courses[course])
            print(user_id)
            print(course.course_id)
            courses_pass.append(count_course_pass(user_id, course.course_id))
        print(courses_pass)
        # print(len(courses))

        return render(request, 'usercourses.html', context={"courses": zip(courses, courses_pass)})
    return HttpResponse("teacher_courses")


def user_course_id(request, id_course):
    user_id = request.session.get('user_id')
    if user_id and Course.objects.filter(id=id_course):
        print(user_id, id_course)
        count = count_course_pass(user_id, id_course)
        return HttpResponse(f"Результат проходження курсу: {count}%")


def teacher_add_courses(request):
    return HttpResponse("teacher_add_course")


def teacher_delete_id(request, id):
    return HttpResponse("teacher_delete_id")


def student_wishlist(request):
    return HttpResponse("wishlist")
