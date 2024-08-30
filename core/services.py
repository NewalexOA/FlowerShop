from core.models import Order, OrderProduct


class OrderService:
    def get_order_details(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_details = (f"Заказ №{order.id}\n"
                             f"Пользователь: {order.user.username}\n"
                             f"Адрес доставки: {order.delivery_address}\n"
                             "Товары:\n")
            for item in OrderProduct.objects.filter(order=order):
                order_details += f"- {item.product.name} (количество: {item.quantity})\n"
            order_details += f"Комментарий: {order.comment}\n"
            return order_details
        except Order.DoesNotExist:
            return None

    def send_order_notification(self, order_id):
        # Логика для отправки уведомления в Telegram
        order_details = self.get_order_details(order_id)
        if order_details:
            from core.bot import bot  # Импортируем bot из core.bot
            bot.send_message('your_chat_id', order_details)
