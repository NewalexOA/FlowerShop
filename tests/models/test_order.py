from core.tests import BaseTestCase
from core.models import Order

class OrderModelTest(BaseTestCase):
    def test_create_order(self):
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.delivery_address, "ул. Тестовая, дом 1")
        self.assertEqual(self.order.comment, "Без комментариев")
        self.assertEqual(self.order.products.count(), 1)
        self.assertIn(self.product, self.order.products.all())
