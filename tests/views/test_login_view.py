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
