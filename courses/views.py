import mimetypes
from email.message import EmailMessage
from itertools import chain

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import redirect
from datetime import datetime

from courses.models import Video
from profiles.views import student_check, get_wishlist, rating_course
from .form import EnrollForm, DeleteForm, TestForm
from .models import Category, Course, Module, Lection, Test, Question, Answer, UserCourse, UserTest
import smtplib
from profiles.views import count_course_mark
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A5


def if_user_has_course(user_id, course_id):
    user_course = UserCourse.objects.filter(user_id=user_id, course_id=course_id)
    return user_course.exists()


def enroll_course(request):
    form_enroll = EnrollForm(request.POST)
    form_delete = DeleteForm(request.POST)
    if form_enroll.is_valid():
        if form_enroll.cleaned_data['course_enroll']:
            now = datetime.now()
            course_id = form_enroll.cleaned_data['course_enroll']
            user = request.user
            course = Course.objects.get(id=course_id)
            user_course = UserCourse.objects.filter(user_id=user, course_id=course)
            if not user_course:
                a = UserCourse(date_start=now.strftime("%Y-%m-%d %H:%M"), user=user, course=course)
                a.save()
                form_enroll.cleaned_data['course_enroll'] = None
    if form_delete.is_valid():
        if form_delete.cleaned_data['course_delete']:
            course_id = form_delete.cleaned_data['course_delete']
            user = request.user
            course = Course.objects.get(id=course_id)
            user_course = UserCourse.objects.filter(user_id=user, course_id=course)
            if user_course:
                if user_course.first().certified:
                    return 'Ви не можете покинути пройдений курс.'
                else:
                    user_course.delete()
                    form_delete.cleaned_data['course_delete'] = None


def courses_index(request):
    categories = Category.objects.select_related()
    courses = Course.objects.filter()
    if request.GET.get('category'):
        courses = Course.objects.filter(category_id=request.GET.get('category'))
        if not courses:
            raise Http404
    if request.GET.get('search'):
        courses = Course.objects.none()
        search_text = request.GET.get('search')
        categories_search = Category.objects.filter(name__icontains=search_text)
        for category_search in categories_search:
            course_search = Course.objects.filter(category_id=category_search.id)
            if course_search:
                courses = chain(course_search, courses)
        courses_search_name = Course.objects.filter(name__icontains=search_text)
        courses_search_descr = Course.objects.filter(description__icontains=search_text)
        courses = chain(courses_search_name, courses_search_descr, courses)
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            error = enroll_course(request)
            if error:
                return render(request, 'error.html', context={'error': error})
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
    wishlist = get_wishlist(request)
    return render(request, 'courses.html',
                  context={"courses": show_course_enroll, "categories": categories, "wishlist": wishlist,
                           'user': request.user})


def courses_search(request, name):
    courses = Course.objects.filter(name=name)
    if courses:
        return render(request, 'courses.html', context={"courses": courses, 'user': request.user})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})
    # return HttpResponseNotFound("not found")


@login_required
@user_passes_test(student_check)
def course_modules(request, id):
    user = request.user
    if not if_user_has_course(user.id, id):
        return HttpResponseNotFound("not found")
    course = Course.objects.filter(id=id)
    if course:
        modules = Module.objects.filter(course_id=course[0].id)
        return render(request, 'course_modules.html',
                      context={"course": course[0], "modules": modules, 'user': request.user})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})


@login_required
@user_passes_test(student_check)
def courses_id_module_id_lecture(request, id, id_module, id_lecture):
    user = request.user
    next_lecture = ''
    prev_lecture = ''
    n_lec = id_lecture + 1
    p_lec = id_lecture - 1
    if Lection.objects.filter(module_id=id_module, id=n_lec):
        next_lecture = id_lecture + 1
    if Lection.objects.filter(module_id=id_module, id=p_lec):
        prev_lecture = id_lecture - 1
    if not if_user_has_course(user.id, id):
        return HttpResponseNotFound("not found")
    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    modules = Module.objects.filter(course_id=id)
    lections = Lection.objects.filter(module_id=id_module)
    tests = Test.objects.filter(module_id=id_module)

    if module and course:
        lectures = Lection.objects.filter(module_id=id_module, id=id_lecture)
        return render(request, 'lecture.html',
                      context={"course": course[0], "module": module[0], 'lections': lections, 'tests': tests,
                               'modules': modules, 'lecture': lectures[0], 'user': request.user,
                               'next_lecture': next_lecture, 'prev_lecture': prev_lecture})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})
    # return HttpResponseNotFound("not found")


def courses_id(request, id):
    rating = rating_course(id)
    show_btn_modules = False
    course = Course.objects.filter(id=id)
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            error = enroll_course(request)
            if error:
                return render(request, 'error.html', context={'error': error})
        else:
            return redirect('login')
    show_enroll = True
    is_over = False
    if user.is_authenticated:
        user_course = UserCourse.objects.filter(user_id=user.id, course_id=id)
        if if_user_has_course(user.id, id):
            show_enroll = False
            is_over = user_course.first().certified
            show_btn_modules = True
    if course:
        modules = Module.objects.filter(course_id=course[0].id)
        wishlist = get_wishlist(request)
        return render(request, 'course.html', context={"course": course[0], "modules": modules,
                                                       "show_enroll": show_enroll, 'user': request.user,
                                                       "show_btn_modules": show_btn_modules, 'wishlist': wishlist,
                                                       'rating': rating, 'is_over': is_over})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})
    # return HttpResponseNotFound("not found")


def courses_category(request, name):
    category = Category.objects.filter(name=name)
    if category:
        category_id = category.first().id
        courses_by_category = Course.objects.filter(category_id=category_id)
        if courses_by_category is not None:
            return render(request, 'courses.html',
                          context={"courses": courses_by_category, 'category': name, 'user': request.user})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})
    # return HttpResponseNotFound("not found")


@login_required
@user_passes_test(student_check)
def courses_id_module_id(request, id, id_module):
    user = request.user
    next_mod = ''
    prev_mod = ''
    n_mod = id_module + 1
    p_mod = id_module - 1
    if Module.objects.filter(id=n_mod):
        next_mod = id_module + 1
    if Module.objects.filter(id=p_mod):
        prev_mod = id_module - 1
    if not if_user_has_course(user.id, id):
        return render(request, 'error.html',
                      context={'error': 'Для перегляду модулів курсу спочатку зареєструйтесь на курс'})
        # return HttpResponseNotFound("Для перегляду модулів курсу спочатку зареєструйтесь на курс.")
    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    if module and course:
        lections = Lection.objects.filter(module_id=id_module)
        tests = Test.objects.filter(module_id=id_module)
        return render(request, 'module.html',
                      context={"course": course[0], "module": module[0], "lections": lections, 'tests': tests,
                               'user': request.user, 'prev_mod': prev_mod, 'next_mod': next_mod})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})


@login_required
@user_passes_test(student_check)
def courses_id_module_id_test(request, id, id_module, id_test):
    user = request.user
    message_course_over = False
    course = Course.objects.filter(id=id)
    module = Module.objects.filter(id=id_module, course_id=id)
    if not if_user_has_course(user.id, id):
        return HttpResponseNotFound("Для проходження тестів курсу спочатку зареєструйтесь на курс.")
    if user.is_authenticated:
        user_test = UserTest.objects.filter(test_id=id_test, user_id=user.id)
        if user_test:
            user_test = user_test[0]
            # return HttpResponse(f"Ви вже проходили цей тест. Ваша оцінка: {user_test.grade}%.")
            return render(request, 'passed_test.html',
                          context={"grade": user_test.grade, "course_id":course[0].id})
    if request.method == 'POST':
        print(request.POST)
        count_questions = Question.objects.filter(test_id=id_test).count()
        form_test = TestForm(request.POST)
        user_answers = {}
        if form_test.is_valid():
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
            member = UserTest(grade=grade, test_id=id_test, user_id=user.id)
            member.save()
            count_tests = 0
            count_user_tests = 0
            for module in course[0].modules.all():
                test = Test.objects.filter(module_id=module.id)
                count_tests += test.count()
                for test_item in test:
                    user_tests = UserTest.objects.filter(test_id=test_item.id, user_id=user.id)
                    count_user_tests += user_tests.count()
            if count_user_tests >= count_tests:
                user_course = UserCourse.objects.filter(user_id=user.id, course_id=course[0].id).first()
                user_course.certified = 1
                user_course.save()
                message_course_over = True
            return render(request, 'result_test.html',
                          context={"mark": mark, "count_questions": count_questions,
                                   "message_course_over": message_course_over, "course_id":course[0].id})

    if module and course:
        tests = Test.objects.filter(module_id=id_module, id=id_test)
        questions = Question.objects.filter(test_id=id_test)
        return render(request, 'test.html',
                      context={"course": course[0], "module": module[0], 'test': tests[0], 'questions': questions,
                               'user': request.user})
    return render(request, 'error.html', context={'error': 'Уппс, щось сталось))'})
    # return HttpResponseNotFound("not found")


def video(request):
    videos = Video.objects.filter()
    return render(request, 'vid.html', context={"videos": videos, 'user': request.user})


def certificate(request, id):
    course = Course.objects.filter(id=id)
    user = request.user
    rating = rating_course(id)
    if user.is_authenticated and Course.objects.filter(id=id):
        mark = count_course_mark(user.id, id)
    return render(request, 'certificate.html', context={'course': course[0], 'user': user,'mark':mark})


def make_certificate(user, course):
    mark = str(count_course_mark(user.id, course[0].id))
    participant_name = str(user.name) + ' ' + str(user.surname)
    font_path = "Helvetica"
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A5), bottomup=0)

    # Задаємо шрифт, розмір і колір для заголовка сертифіката
    p.setFont(font_path, 24)
    p.setFillColor(colors.black)
    p.drawCentredString(A5[1] / 2, 100, "Learniverse certificate")

    # Задаємо шрифт, розмір і колір для тексту про видачу сертифіката
    p.setFont(font_path, 16)
    p.setFillColor(colors.black)
    p.drawCentredString(A5[1] / 2, 150, "This certificate is issued for successful completion of the course:")

    p.setFont(font_path, 20)
    p.setFillColor(colors.blue)
    p.drawCentredString(A5[1] / 2, 180, f"«{course[0].name}»")

    p.setFont(font_path, 16)
    p.setFillColor(colors.black)
    p.drawCentredString(A5[1] / 2, 210, f"With a score of: {mark}%")

    p.setFont(font_path, 24)
    p.setFillColor(colors.black)
    p.drawCentredString(A5[1] / 2, 250, participant_name)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def generate_certificate(request, id):
    user = request.user
    course = Course.objects.filter(id=id)
    buffer = make_certificate(user, course)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Learniverse_certificate.pdf"'
    return response


def send_certificate(request, id):
    user = request.user
    course = Course.objects.filter(id=id)
    buffer = make_certificate(user, course)
    attachment_filename = "certificate.pdf"
    body = f"Сертифікат за успішне проходження курсу '{course[0].name}'"
    sender = 'systems.kpi@gmail.com'
    password = 'ivrtnhxzvdiunfuu'
    receiver = user.email
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'Сертифікат Learniverse'

    message.add_attachment(body, 'plain')
    maintype, _, subtype = (mimetypes.guess_type(attachment_filename)[0] or 'application/octet-stream').partition("/")

    message.add_attachment(buffer.read(), maintype=maintype, subtype=subtype, filename=attachment_filename)

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    return render(request, 'error.html', context={'error': 'Сертифікат було надіслано!'})
