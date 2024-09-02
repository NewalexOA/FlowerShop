from core.models import Order, BotSettings, Product, Cart, CartProduct
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
        # Добавление товара в корзину
        product = Product.objects.create(name="Test Product", price=10.00)
        cart, created = Cart.objects.get_or_create(user=self.user)
        CartProduct.objects.create(cart=cart, product=product, quantity=1)

        self.client.login(username='testuser', password='12345')

        response = self.client.post(reverse('checkout'), {
            'address': '123 Test St',
            'comment': 'Test Comment'
        })

        self.assertRedirects(response, reverse('order_complete'))
        
        # Проверяем, что был создан новый заказ
        new_order = Order.objects.latest('id')
        self.assertEqual(new_order.delivery_address, '123 Test St')
        self.assertEqual(new_order.comment, 'Test Comment')
        
        mock_send_message.assert_called_once_with(admin_chat_id, ANY)
