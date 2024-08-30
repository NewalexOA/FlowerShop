from django.test import TestCase
from core.models import Product

class ProductModelTest(TestCase):

    def test_create_product(self):
        product = Product.objects.create(
            name="Роза",
            description="Красная роза",
            price=100.00
        )
        self.assertEqual(product.name, "Роза")
        self.assertEqual(product.description, "Красная роза")
        self.assertEqual(product.price, 100.00)
