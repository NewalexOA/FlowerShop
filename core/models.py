from django.db import models
from django.contrib.auth.models import User
import base64

# Модель для товаров (букетов)
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.TextField(verbose_name="Изображение", blank=True, null=True)

    def __str__(self):
        return self.name

    def save_image(self, image_file):
        self.image = base64.b64encode(image_file.read()).decode('utf-8')

    def get_image(self):
        if self.image:
            return base64.b64decode(self.image)
        return None

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

# Модель для корзины
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, through='CartProduct', verbose_name="Товары")

    def __str__(self):
        return f"Корзина {self.user.username}"

# Модель для продуктов в корзине
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} в корзине {self.cart.user.username}"

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

# Модель для заказов
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    products = models.ManyToManyField(Product, through='OrderProduct', verbose_name="Товары")
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

# Промежуточная модель для связи товаров с заказами
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} в заказе {self.order.id}"

    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"


class BotSettings(models.Model):
    admin_chat_id = models.CharField(max_length=50, verbose_name="Admin Chat ID")

    def __str__(self):
        return f"Настройки бота (ID: {self.id})"
    
    class Meta:
        verbose_name = "Настройки бота"
        verbose_name_plural = "Настройки бота"