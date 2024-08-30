from django.test import TestCase
from unittest.mock import patch, ANY
from core.bot import setup_bot, send_order_notification
from core.models import Order, Product, OrderProduct
from django.contrib.auth.models import User

class TelegramBotTest(TestCase):
    @patch('core.bot.bot.polling')
    def test_bot_initialization(self, mock_polling):
        # Проверяем, что бот инициализируется и запускается без фактического опроса сервера
        setup_bot()
        mock_polling.assert_called_once()

    @patch('core.bot.bot.send_message')
    def test_send_order_notification(self, mock_send_message):
        # Создаем пользователя и продукт
        user = User.objects.create(username='testuser')
        product = Product.objects.create(name='Test Product', price=10.00)

        # Создаем заказ
        order = Order.objects.create(user=user, delivery_address='123 Test St')
        OrderProduct.objects.create(order=order, product=product, quantity=1)

        # Используем ID созданного заказа
        print(f"Order ID: {order.id}")  # Отладочная печать
        send_order_notification(order.id)

        # Проверяем, что send_message был вызван с нужными параметрами
        mock_send_message.assert_called_once_with('your_chat_id', ANY)
        print("send_order_notification called")
        if mock_send_message.called:
            print("send_message called")
        else:
            print("send_message NOT called")
