from core.tests import BaseTestCase
from unittest.mock import patch, ANY
from core.bot import send_order_notification
from config import admin_chat_id
from core.models import BotSettings

class TelegramBotTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        BotSettings.objects.create(admin_chat_id=admin_chat_id)

    @patch('core.bot.bot.send_message')
    def test_send_order_notification(self, mock_send_message):
        send_order_notification(self.order.id)
        mock_send_message.assert_called_once_with(admin_chat_id, ANY)
