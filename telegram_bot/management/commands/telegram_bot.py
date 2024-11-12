import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import TeleBot

from telegram_bot.handlers import init_handlers

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


class Command(BaseCommand):
    """Запуск телеграм-бота."""
    help = "Запустить телеграм бота."

    def handle(self, *args, **kwargs) -> None:
        """Обработка команды."""
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        init_handlers(bot)
        logging.info("Запуск бота.")
        bot.infinity_polling()
