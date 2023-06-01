from django.test import TestCase
from django.urls import reverse

from django.test.client import RequestFactory

from main.views import main_about, main_index
from profiles.models import User


# Create your tests here.
class MainTestCase(TestCase):
    def setUp(self):
        # self.factory = RequestFactory()
        self.user = User.objects.create(name='testuser', surname='testuser', email="a.k@gmail.com",
                                        date_birth='2002-12-12', password='1234', phone_number='0968956432',
                                        role="student", description='descr')

    def test_main_about(self):
        url = reverse('about')  # Переконайтеся, що це правильний URL шлях до сторінки "about.html"
        self.client.force_login(self.user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertEqual(response.context['user'], self.user)

    def test_main_index_authenticated_user(self):
        url = reverse('main')
        self.client.force_login(self.user)

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['user'], self.user)

    def test_main_index_unauthenticated_user(self):
        url = reverse('main')

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
