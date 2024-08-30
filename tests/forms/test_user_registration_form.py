from django.test import TestCase
from core.forms import UserRegisterForm

class UserRegisterFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',  # Добавлено поле email
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)

        # Проверяем, что форма валидна
        if not form.is_valid():
            print("Форма не валидна. Ошибки:", form.errors)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',  # Добавлено поле email
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = UserRegisterForm(data=form_data)

        # Ожидаем, что форма будет невалидна из-за несовпадения паролей
        self.assertFalse(form.is_valid())
