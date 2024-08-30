from django.test import TestCase
from unittest.mock import patch, ANY
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Order, Product, OrderProduct

class CheckoutViewTest(TestCase):
    @patch('core.bot.bot.send_message')
    def test_checkout_view(self, mock_send_message):
        # Создаем пользователя и аутентифицируем его
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Создаем продукт и добавляем его в сессию корзины
        product = Product.objects.create(name='Test Product', price=10.00)
        session = self.client.session
        session['cart'] = [product.id]
        session.save()

        # Выполняем POST-запрос на checkout
        response = self.client.post(reverse('checkout'), {
            'address': '123 Test St',
            'comment': 'Test Comment'
        })

        # Убедимся, что заказ был создан
        order = Order.objects.first()
        print(f"Order created with ID: {order.id}")  # Отладочный вывод

        # Проверка редиректа
        self.assertRedirects(response, reverse('order_complete'))

        # Проверяем, что send_order_notification вызвал send_message
        print("send_order_notification called")
        mock_send_message.assert_called_once()
        if mock_send_message.called:
            print("send_message called")
        else:
            print("send_message NOT called")
