from core.models import Order, BotSettings
from core.tests import BaseTestCase
from django.urls import reverse
from unittest.mock import patch, ANY
from config import admin_chat_id

class CheckoutViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        BotSettings.objects.create(admin_chat_id=admin_chat_id)

    @patch('core.bot.bot.send_message')
    def test_checkout_view(self, mock_send_message):
        self.client.login(username='testuser', password='12345')

        session = self.client.session
        session['cart'] = [self.product.id]
        session.save()

        response = self.client.post(reverse('checkout'), {
            'address': '123 Test St',
            'comment': 'Test Comment'
        })

        order = Order.objects.first()
        self.assertRedirects(response, reverse('order_complete'))
        mock_send_message.assert_called_once_with(admin_chat_id, ANY)
