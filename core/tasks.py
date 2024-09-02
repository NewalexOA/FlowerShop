from django.conf import settings
import logging
import telebot
from .models import Order, OrderProduct, BotSettings

logger = logging.getLogger(__name__)

def send_order_notification(order_id):
    try:
        logger.info(f"Starting send_order_notification for order_id: {order_id}")
        
        # Получение токена бота из настроек Django
        bot_token = settings.TELEGRAM_BOT_TOKEN
        logger.debug(f"Bot token retrieved from settings: {bot_token[:5]}...")  # Логируем только первые 5 символов токена для безопасности

        # Получение настроек бота из базы данных
        bot_settings = BotSettings.objects.first()
        if not bot_settings or not bot_settings.admin_chat_id:
            logger.error("Admin chat ID is not set in the database.")
            return

        admin_chat_id = bot_settings.admin_chat_id
        logger.debug(f"Admin chat ID retrieved: {admin_chat_id}")

        # Получение информации о заказе
        order = Order.objects.get(id=order_id)
        order_details = f"Заказ №{order.id}\nПользователь: {order.user.username}\nАдрес доставки: {order.delivery_address}\n"
        order_details += "Товары:\n"
        for item in OrderProduct.objects.filter(order=order):
            order_details += f"- {item.product.name} (количество: {item.quantity})\n"
        order_details += f"Комментарий: {order.comment if order.comment else 'Нет комментариев'}\n"

        logger.debug(f"Order details prepared: {order_details}")

        # Инициализация бота
        bot = telebot.TeleBot(bot_token)
        
        # Отправка сообщения администратору
        bot.send_message(admin_chat_id, order_details)
        logger.info(f"Order notification sent for order ID: {order_id}")
    except Exception as e:
        logger.error(f"Failed to send order notification: {str(e)}", exc_info=True)
        