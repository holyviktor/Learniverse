from django.test import TestCase
from django.urls import reverse
from courses.models import UserCourse, Category, Course, Module, Test, UserTest
from profiles.form import SignUpForm
from profiles.models import User
from profiles.views import Rating, count_course_mark, rating_course, count_course_pass, get_wishlist

from django.test.client import RequestFactory
# Create your tests here.
class ProfileTestCase(TestCase):


    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')

        self.user1 = User.objects.create(name='testuser1', surname='testuser1', email="test1@gmail.com",
                                         date_birth='2002-08-12', password='12211', phone_number='0667236485',
                                         role="student", description='descr')

        self.user2 = User.objects.create(name='testuser2', surname='testuser2', email="test2@gmail.com",
                                         date_birth='2002-08-12', password='1111', phone_number='0667236485',
                                         role="student", description='descr')

        self.category = Category.objects.create(name="Category")
        self.course = Course.objects.create(name='Math', duration="5", category=self.category, teacher_id=1,
                                            description="vv")
        self.coursev = Course.objects.create(name='IT', duration="6", category=self.category, teacher_id=1,
                                            description="vv")

        UserCourse.objects.create(date_start="2022-12-12", certified=0, user=self.user1, course=self.course)
        UserCourse.objects.create(date_start="2022-12-09", certified=0, user=self.user2, course=self.course)
        self.course1 = UserCourse.objects.create(date_start="2022-12-08", certified=0, user=self.user,
                                                 course=self.course)
        self.course2 = UserCourse.objects.create(date_start="2022-12-08", certified=0, user=self.user,
                                                 course=self.coursev)

        self.module1 = Module.objects.create(course=self.course, name='Module 1', duration=1, course_id=1)
        self.module2 = Module.objects.create(course=self.course, name='Module 2', duration=1, course_id=1)

        self.test1 = Test.objects.create(module=self.module1, title='Test 1')
        self.test2 = Test.objects.create(module=self.module2, title='Test 2')

        self.register_url = reverse('sign_up')

    def test_rating_course(self):
        expected_result = [
            Rating(user=self.user1, total_mark=count_course_mark(self.user1.id, self.course.id)),
            Rating(user=self.user2, total_mark=count_course_mark(self.user2.id, self.course.id)),
            Rating(user=self.user, total_mark=count_course_mark(self.user.id, self.course.id))
        ]
        result = rating_course(self.course.id)
        self.assertEqual(len(result), len(expected_result))
        for expected, actual in zip(expected_result, result):
            self.assertEqual(expected.user, actual.user)
            self.assertEqual(expected.total_mark, actual.total_mark)

    def test_count_course_mark_no_tests(self):
        result = count_course_mark(self.user.id, self.course.id)
        self.assertEqual(result, 0)

    def test_count_course_mark_with_tests(self):
        UserTest.objects.create(user=self.user, test=self.test1, grade=80)
        UserTest.objects.create(user=self.user, test=self.test2, grade=90)
        result = count_course_mark(self.user.id, self.course.id)
        self.assertEqual(result, 85)

    def test_count_course_pass_no_tests(self):
        result = count_course_pass(self.user.id, self.course.id)
        self.assertEqual(result, 0)

    def test_count_course_pass_with_tests(self):
        UserTest.objects.create(user=self.user, test=self.test1, grade=80)
        result = count_course_pass(self.user.id, self.course.id)
        self.assertEqual(result, 50)

        UserTest.objects.create(user=self.user, test=self.test2, grade=90)
        result = count_course_pass(self.user.id, self.course.id)
        self.assertEqual(result, 100)

    def test_profiles_index_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user.html')
        self.assertEqual(response.context['user'], self.user)

    def test_profiles_index_unauthenticated_user(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login')+f'?next=/profile/')

    def test_profiles_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertIsInstance(response.context['form'], SignUpForm)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_profiles_register_view_post_valid_form(self):
        data = {
            'name': ['Ivanna'], 'surname': ['Karaim'], 'date_birth': ['2003-07-08'], 'phone_number': ['0667236485'],
            'email': ['karaimivanna@gmail.com'], 'password': ['1111111111111'],
            'description': ['Це вікно підійде вашій оселі, ']
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(User.objects.filter(email='karaimivanna@gmail.com').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profiles_register_view_post_invalid_form(self):
        data = {
            'name': ['Ivanna'], 'surname': ['111'], 'date_birth': ['2003-07-08'], 'phone_number': ['0667236485'], 'email': ['karaimivanna@gmail.com'], 'password': ['1111111111111'], 'description': ['Це вікно підійде вашій оселі, ']
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        self.assertIsInstance(response.context['form'], SignUpForm)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'form', 'surname', 'неправильно введено прізвище')

    def test_profiles_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {'email': 'a.k@gmail.com', 'password': '1234'})
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profiles_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'email': 'a.k@gmail.com', 'password': 'wrongpassword'})
        self.assertTemplateUsed(response, 'login.html')
        self.assertFormError(response, 'form', 'password', 'Неправильно введений пароль')

    def test_profiles_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('main'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_courses_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile_courses'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.course.name)
        self.assertContains(response, self.coursev.name)


    def test_user_courses_unauthenticated_user(self):
        response = self.client.get(reverse('profile_courses'))

        self.assertRedirects(response, reverse('login')+f'?next=/profile/courses')

    def test_user_course_id_authenticated_student(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('user_course', args=[1]))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Результат прогресу курсу:')
        self.assertContains(response, 'оцінка за курс:')

    def test_user_course_id_unauthenticated_user(self):

        response = self.client.get(reverse('user_course', args=[1]))
        self.assertRedirects(response, reverse('login')+f'?next=/profile/course/1')

    def test_student_wishlist_authenticated_user(self):

        self.client.force_login(self.user)

        # Set the Wishlist_user cookie with the IDs of course1 and course2
        wishlist_cookie = ','.join([str(self.course.id), str(self.coursev.id)])
        self.client.cookies['Wishlist_user'] = wishlist_cookie

        response = self.client.get(reverse('wishlist'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Math')
        self.assertContains(response, 'IT')

    def test_student_wishlist_empty_wishlist(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Course')

    def test_student_wishlist_invalid_course_id(self):
        self.client.force_login(self.user)
        wishlist_cookie = '999'
        self.client.cookies['Wishlist_user'] = wishlist_cookie
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)

    def test_change_wishlist_add_course(self):
        initial_wishlist_cookie = '1,2'
        self.client.cookies['Wishlist_user'] = initial_wishlist_cookie
        response = self.client.post(reverse('like'), {'id': 3})
        self.assertEqual(response.status_code, 302)
        updated_wishlist_cookie = response.cookies['Wishlist_user'].value
        self.assertEqual(updated_wishlist_cookie, '1,2,3')

    def test_change_wishlist_remove_course(self):
        initial_wishlist_cookie = '1,2,3'
        self.client.cookies['Wishlist_user'] = initial_wishlist_cookie
        response = self.client.post(reverse('like'), {'id': 2})
        self.assertEqual(response.status_code, 302)
        updated_wishlist_cookie = response.cookies['Wishlist_user'].value
        self.assertEqual(updated_wishlist_cookie, '1,3')

    def test_change_wishlist_remove_last_course(self):
        initial_wishlist_cookie = '1'
        self.client.cookies['Wishlist_user'] = initial_wishlist_cookie
        response = self.client.post(reverse('like'), {'id': 1})
        self.assertEqual(response.status_code, 302)

    def test_get_wishlist_with_cookie(self):
        request = self.factory.get(reverse('wishlist'))
        request.COOKIES['Wishlist_user'] = '1,2,3'
        wishlist = get_wishlist(request)
        self.assertEqual(wishlist, [1, 2, 3])

    def test_get_wishlist_without_cookie(self):
        request = self.factory.get('/')
        wishlist = get_wishlist(request)
        self.assertEqual(wishlist, [])
