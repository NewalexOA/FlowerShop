from core.tests import BaseTestCase
from core.models import OrderProduct

class OrderProductModelTest(BaseTestCase):
    def test_create_order_product(self):
        self.assertEqual(self.order_product.order, self.order)
        self.assertEqual(self.order_product.product, self.product)
        self.assertEqual(self.order_product.quantity, 2)

    def test_get_total_price(self):
        self.assertEqual(self.order_product.get_total_price(), 200.00)
