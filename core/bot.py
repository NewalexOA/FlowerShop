import os
import django
import telebot
import threading
from django.conf import settings
from core.models import Order, OrderProduct

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
    order = Order.objects.get(id=order_id)
    order_details = f"Заказ №{order.id}\nПользователь: {order.user.username}\nАдрес доставки: {order.delivery_address}\n"
    order_details += "Товары:\n"
    for item in OrderProduct.objects.filter(order=order):
        order_details += f"- {item.product.name} (количество: {item.quantity})\n"
    order_details += f"Комментарий: {order.comment}\n"

    # Отправка сообщения администратору (замените 'your_chat_id' на реальный chat_id)
    bot.send_message('your_chat_id', order_details)


# Функция запуска бота
def setup_bot():
    bot.polling(none_stop=True)


# Запуск бота в отдельном потоке
bot_thread = threading.Thread(target=setup_bot)
bot_thread.start()
