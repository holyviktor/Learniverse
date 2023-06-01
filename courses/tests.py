from io import BytesIO

from django.test import TestCase, RequestFactory
from django.urls import reverse

from courses.models import UserCourse, Course, Category, Module
from courses.views import if_user_has_course, enroll_course, courses_index, course_modules, make_certificate, \
    generate_certificate, send_certificate
from profiles.models import User


class UserHasCourseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432', role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category,  teacher_id=1, description="vv")

    def test_user_has_course_exists(self):
        UserCourse.objects.create(date_start="2022-12-12", certified=0,user=self.user, course=self.course)
        result = if_user_has_course(self.user.id, self.course.id)
        self.assertTrue(result)

    def test_user_has_course_not_exists(self):
        result = if_user_has_course(self.user.id, self.course.id)
        self.assertFalse(result)


class CoursesIndexTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")


    def test_courses_index_no_filter(self):
        self.client.force_login(self.user)
        url = reverse('courses')
        response = self.client.post(url)
        self.client.force_login(self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['courses']), 1)

    def test_courses_index_category_filter(self):
        self.client.force_login(self.user)
        url = reverse('courses') + f'?category={self.course.id}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['courses']), 1)

    def test_courses_index_search_filter(self):
        self.client.force_login(self.user)
        url = reverse('courses') + f'?search={self.course.name}'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['courses']), 1)

    def test_courses_index_authenticated_user(self):
        request = self.factory.post('/courses')
        request.user = self.user
        response = courses_index(request)
        self.assertEqual(response.status_code, 200)


class CourseModulesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,description="vv")

        self.module1 = Module.objects.create(course=self.course, name='Module 1', duration=1, course_id=1)
        self.module2 = Module.objects.create(course=self.course, name='Module 2', duration=1, course_id=1)

    def test_course_modules_with_authenticated_user_and_valid_course(self):
        self.client.force_login(self.user)
        UserCourse.objects.create(date_start="2022-12-12", certified=0, user=self.user, course=self.course)
        url = reverse('module', args=[self.course.id, self.module1.id])
        response = self.client.get(url)
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertIn('course', response.context)
        self.assertIn('module', response.context)
        course = response.context['course']
        self.assertEqual(course, self.course)

    def test_course_modules_with_authenticated_user_and_invalid_course(self):
        self.client.force_login(self.user)
        invalid_course_id = self.course.id + 1
        url = reverse('module', args=[invalid_course_id, self.module1.id+100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_course_modules_with_unauthenticated_user(self):
        url = reverse('module', args=[self.course.id, self.module1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login')+f"?next=/courses/{self.course.id}/module/{self.module1.id}")


class CoursesIdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")

    def test_courses_id(self):
        self.client.force_login(self.user)
        url = reverse('course', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course.html')
        self.assertIn('course', response.context)
        course = response.context['course']
        self.assertEqual(course, self.course)


class CertificateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")

    def test_certificate(self):
        self.client.force_login(self.user)
        url = reverse('certificate', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certificate.html')
        self.assertIn('course', response.context)
        course = response.context['course']
        self.assertEqual(course, self.course)


class MakeCertificateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")
    def test_make_certificate(self):
        certificate = make_certificate(self.user, [self.course])
        self.assertIsInstance(certificate, BytesIO)
        pdf_content = certificate.getvalue()
        self.assertGreater(len(pdf_content), 0)


class GenerateCertificateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")

    def test_generate_certificate(self):
        request = self.factory.get('/generate-certificate/')
        request.user = self.user
        response = generate_certificate(request, self.course.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(
            response['Content-Disposition'], 'attachment; filename="Learniverse_certificate.pdf"'
        )



class SendCertificateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')
        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")

    def test_send_certificate(self):
        request = self.factory.get('/send-certificate/')
        request.user = self.user
        response = send_certificate(request, self.course.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Сертифікат було надіслано!')

