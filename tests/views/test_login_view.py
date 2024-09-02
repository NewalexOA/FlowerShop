from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345',
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_view_invalid_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пожалуйста, введите правильные имя пользователя и пароль.")

    def test_login_view_nonexistent_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пожалуйста, введите правильные имя пользователя и пароль.")
