from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Order, Product

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name="Роза",
            description="Красная роза",
            price=100.00
        )

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            delivery_address="ул. Тестовая, дом 1",
            comment="Без комментариев"
        )
        order.products.add(self.product)

        self.assertEqual(order.user.username, "testuser")
        self.assertEqual(order.delivery_address, "ул. Тестовая, дом 1")
        self.assertEqual(order.comment, "Без комментариев")
        self.assertEqual(order.products.count(), 1)
        self.assertIn(self.product, order.products.all())
