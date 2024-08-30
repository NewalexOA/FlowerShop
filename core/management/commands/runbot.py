from django.core.management.base import BaseCommand
from core.bot import setup_bot

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        setup_bot()
