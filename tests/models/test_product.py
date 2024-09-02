from core.tests import BaseTestCase
from core.models import Product

class ProductModelTest(BaseTestCase):
    def test_create_product(self):
        self.assertEqual(self.product.name, "Роза")
        self.assertEqual(self.product.description, "Красная роза")
        self.assertEqual(self.product.price, 100.00)
