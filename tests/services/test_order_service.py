from django.test import TestCase
from core.models import Order, User
from core.services import OrderService

class OrderServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.order = Order.objects.create(user=self.user, delivery_address='Test Address')
        self.service = OrderService()

    def test_get_order_details(self):
        details = self.service.get_order_details(self.order.id)
        self.assertIn('Заказ №', details)
        self.assertIn('Пользователь: testuser', details)

    def test_get_order_details_invalid_id(self):
        details = self.service.get_order_details(999)  # Несуществующий ID
        self.assertIsNone(details)
