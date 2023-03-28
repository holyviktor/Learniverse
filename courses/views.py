from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Category, Course


# Create your views here.
def courses_index(request):
    return HttpResponse("courses")


def courses_id(request, id):
    course = Course.objects.filter(id=id)
    print(course)
    if course is not None:

        return render(request, 'course.html', context={"course": course[0]})
    raise Http404('')


def courses_category(request, name):
    category = Category.objects.filter(name=name)
    if category is not None:
        category_id = category.first().id
        courses_by_category = Course.objects.filter(category_id=category_id)
        if courses_by_category is not None:
            return render(request, 'courses.html', context={"courses": courses_by_category, 'category': name})


def courses_search(request, name):
    return HttpResponse(f"search {name}")


def courses_id_modules(request, id):
    return HttpResponse("id_modules")


def courses_id_module_id(request, id, id_module):
    return HttpResponse("id_modules")


def courses_id_module_id_lecture(request, id, id_module, id_lecture):
    return HttpResponse("courses_id_module_id_lecture")


def courses_id_module_id_test(request, id, id_module, id_test):
    return HttpResponse("courses_id_module_id_test")
