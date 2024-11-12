from telebot import TeleBot

from .handlers import MessageHandler


def init_handlers(bot: TeleBot) -> None:
    MessageHandler(bot)
