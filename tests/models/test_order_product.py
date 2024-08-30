from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Order, Product, OrderProduct

class OrderProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name="Роза",
            description="Красная роза",
            price=100.00
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="ул. Тестовая, дом 1",
            comment="Без комментариев"
        )

    def test_create_order_product(self):
        order_product = OrderProduct.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )

        self.assertEqual(order_product.order, self.order)
        self.assertEqual(order_product.product, self.product)
        self.assertEqual(order_product.quantity, 2)

    def test_get_total_price(self):
        order_product = OrderProduct.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        self.assertEqual(order_product.get_total_price(), 200.00)
