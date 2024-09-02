from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Product, Order, OrderProduct, Cart, CartProduct

class BaseTestCase(TestCase):
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
        self.order_product = OrderProduct.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
