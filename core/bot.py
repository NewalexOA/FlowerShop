import os
import django
import telebot
from django.conf import settings
from core.models import Order, OrderProduct, BotSettings

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FlowerShop.settings')

# Инициализация Django
django.setup()

# Инициализация бота
bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Здравствуйте! Этот бот будет уведомлять вас о новых заказах.')

# Функция для отправки уведомления о новом заказе
def send_order_notification(order_id):
    try:
        # Получение настроек бота
        settings = BotSettings.objects.first()
        if not settings or not settings.admin_chat_id:
            print("Admin chat ID is not set in the database.")
            return

        admin_chat_id = settings.admin_chat_id

        # Получение информации о заказе
        order = Order.objects.get(id=order_id)
        order_details = f"Заказ №{order.id}\nПользователь: {order.user.username}\nАдрес доставки: {order.delivery_address}\n"
        order_details += "Товары:\n"
        for item in OrderProduct.objects.filter(order=order):
            order_details += f"- {item.product.name} (количество: {item.quantity})\n"
        order_details += f"Комментарий: {order.comment if order.comment else 'Нет комментариев'}\n"

        # Отправка сообщения администратору
        bot.send_message(admin_chat_id, order_details)
        print(f"Order notification sent for order ID: {order_id}")
    except Exception as e:
        print(f"Failed to send order notification: {e}")