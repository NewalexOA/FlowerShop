from django.test import TestCase
from core.forms import UserRegisterForm

class UserRegisterFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
