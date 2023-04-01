from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render
from .models import Category, Course, Module, Lection, Test, Question, Answer


# Create your views here.
def courses_index(request):
    return HttpResponse("courses")


def courses_search(request, name):
    return HttpResponse(f"search {name}")


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
        # for question in questions:
        #     answer = question.answers.all()
        #     print(answer)
        # answers = Answer.objects.filter()
        return render(request, 'lecture.html',
                      context={"course": course[0], "module": module[0], 'lecture': lectures[0]})
    return HttpResponseNotFound("not found")


def courses_id(request, id):
    course = Course.objects.filter(id=id)
    print(course)
    if course:
        modules = Module.objects.filter(course_id=course[0].id)
        return render(request, 'course.html', context={"course": course[0], "modules": modules})
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
        return render(request, 'modules.html', context={"course":course[0], "module": module[0], "lections": lections, 'tests': tests})
    return HttpResponseNotFound("not found")


def courses_id_module_id_test(request, id, id_module, id_test):
    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    if module and course:
        tests = Test.objects.filter(module_id=id_module, id=id_test)
        questions = Question.objects.filter(test_id=id_test)
        # for question in questions:
        #     answer = question.answers.all()
        #     print(answer)
        # answers = Answer.objects.filter()
        return render(request, 'test.html',
                      context={"course": course[0], "module": module[0], 'test': tests[0], 'questions':questions})
    return HttpResponseNotFound("not found")




