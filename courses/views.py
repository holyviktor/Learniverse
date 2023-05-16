from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from datetime import datetime

from profiles.models import User
from courses.models import Video
from profiles.views import student_check
from .form import EnrollForm, DeleteForm, TestForm
from .models import Category, Course, Module, Lection, Test, Question, Answer, UserCourse, UserTest


def enroll_course(request):
    form_enroll = EnrollForm(request.POST)
    form_delete = DeleteForm(request.POST)
    print("here?")
    if form_enroll.is_valid():
        if form_enroll.cleaned_data['course_enroll']:

            # print("enroll")
            now = datetime.now()
            course_id = form_enroll.cleaned_data['course_enroll']
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)

            # print(user.id)
            course = Course.objects.get(id=course_id)
            user_course = UserCourse.objects.filter(user_id=user, course_id=course)
            if not user_course:
                # print(course.id)
                # print(now.strftime("%Y/%m/%d %H:%M:%S"))
                a = UserCourse(date_start=now.strftime("%Y-%m-%d %H:%M"), user=user, course=course)
                a.save()
                form_enroll.cleaned_data['course_enroll'] = None
    if form_delete.is_valid():
        if form_delete.cleaned_data['course_delete']:

            # print("delete")
            course_id = form_delete.cleaned_data['course_delete']
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            print(user.id)
            course = Course.objects.get(id=course_id)
            user_course = UserCourse.objects.filter(user_id=user, course_id=course)
            print(user_course)
            if user_course:
                user_course.delete()
                form_delete.cleaned_data['course_delete'] = None
                # return redirect('profile')


# Create your views here.
def courses_index(request):
    categories = Category.objects.select_related()
    if request.GET.get('category'):
        courses = Course.objects.filter(category_id=request.GET.get('category'))
        if not courses:
            raise Http404
    courses = Course.objects.filter()
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        if user_id:
            enroll_course(request)
        else:
            return redirect('login')
    show_course_enroll = {}
    for course in courses:
        if user_id:
            user_course = UserCourse.objects.filter(user_id=user_id, course_id=course.id)
            if user_course:
                show_course_enroll[course] = False
            else:
                show_course_enroll[course] = True
        else:
            show_course_enroll[course] = True
    print(show_course_enroll)
    # return render(request, 'login.html', {'form': form})
    return render(request, 'courses.html', context={"courses": show_course_enroll, "categories": categories})


def courses_search(request, name):
    courses = Course.objects.filter(name=name)
    if courses:
        return render(request, 'courses.html', context={"courses": courses})
    return HttpResponseNotFound("not found")


def course_modules(request, id):
    course = Course.objects.filter(id=id)
    if course:
        modules = Module.objects.filter(course_id=course[0].id)
        return render(request, 'course_modules.html', context={"course": course[0], "modules": modules})
    return HttpResponseNotFound("not found")


def courses_id_module_id_lecture(request, id, id_module, id_lecture):
    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    if module and course:
        lectures = Lection.objects.filter(module_id=id_module, id=id_lecture)
        return render(request, 'lecture.html',
                      context={"course": course[0], "module": module[0], 'lecture': lectures[0]})
    return HttpResponseNotFound("not found")


def courses_id(request, id):
    course = Course.objects.filter(id=id)
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        if user_id:
            enroll_course(request)
        else:
            return redirect('login')
    show_enroll = True
    if user_id:
        user_course = UserCourse.objects.filter(user_id=user_id, course_id=id)
        if user_course:
            show_enroll = False

    if course:
        modules = Module.objects.filter(course_id=course[0].id)
        return render(request, 'course.html', context={"course": course[0], "modules": modules,
                                                       "show_enroll": show_enroll})
    return HttpResponseNotFound("not found")


def courses_category(request, name):
    category = Category.objects.filter(name=name)
    if category:
        category_id = category.first().id
        courses_by_category = Course.objects.filter(category_id=category_id)
        if courses_by_category is not None:
            return render(request, 'courses.html', context={"courses": courses_by_category, 'category': name})
    return HttpResponseNotFound("not found")


def courses_id_module_id(request, id, id_module):
    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    if module and course:
        lections = Lection.objects.filter(module_id=id_module)
        tests = Test.objects.filter(module_id=id_module)
        return render(request, 'module.html',
                      context={"course": course[0], "module": module[0], "lections": lections, 'tests': tests})
    return HttpResponseNotFound("not found")


# @login_required
# @user_passes_test(student_check)
def courses_id_module_id_test(request, id, id_module, id_test):
    user_id = request.session.get('user_id')
    if user_id:
        user_test = UserTest.objects.filter(test_id=id_test, user_id=user_id)
        if user_test:
            user_test = user_test[0]
            return HttpResponse(f"Ви вже проходили цей тест. Ваша оцінка: {user_test.grade}%.")
    if request.method == 'POST':
        count_questions = Question.objects.filter(test_id=id_test).count()
        form_test = TestForm(request.POST)
        user_answers = {}
        if form_test.is_valid():
            # print("here!")
            mark = 0
            questions = Question.objects.filter(test_id=id_test)
            print(questions)
            for question in questions:
                if str(question.id) in form_test.data:
                    user_answers[question.id] = form_test.data[str(question.id)]
                    answer = Answer.objects.filter(id=int(form_test.data[str(question.id)]))[0]
                    # print(answer.title)
                    # print(answer.correctness)
                    if answer.correctness:
                        mark += 1
            grade = mark / count_questions * 100
            member = UserTest(grade=grade, test_id=id_test, user_id=user_id)
            member.save()
            return HttpResponse(f"Your mark is {mark}/{count_questions}")

    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    if module and course:
        tests = Test.objects.filter(module_id=id_module, id=id_test)
        questions = Question.objects.filter(test_id=id_test)
        return render(request, 'test.html',
                      context={"course": course[0], "module": module[0], 'test': tests[0], 'questions': questions})
    return HttpResponseNotFound("not found")


def video(request):
    videos = Video.objects.filter()
    return render(request, 'vid.html', context={"videos": videos})
