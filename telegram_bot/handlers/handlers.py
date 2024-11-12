import logging

from typing import Callable, Optional

from telebot import TeleBot
from telebot.types import (
    Message,
    User,
    CallbackQuery,
)

from telegram_bot.keyboard import KeyboardMarkup

from src.application.infrastructure.dto.user import (
    UserDTO,
    UserCreateDTO,
)
from src.application.infrastructure.dto.dto import (
    WalletDTO,
    WalletCreateDTO,
)
from src.application.repository.repository import (
    UserRepository,
    TransactionRepository,
    WalletRepository,
)


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MessageHandler:
    """Обработчик сообщений."""

    def __init__(self, bot: TeleBot) -> None:
        self.bot = bot
        self.register_handlers()
        self.keyboard_markup = KeyboardMarkup()

        self.user_repository = UserRepository
        self.wallet_repository = WalletRepository
        self.transaction_repository = TransactionRepository

    def register_handlers(self) -> None:
        logger.info("Инициализация обработчиков.")
        self.bot.message_handler(commands=["help"])(self.handle_help)
        self.bot.message_handler(commands=["start"])(self.handle_start)
        self.bot.callback_query_handler(func=lambda call: True)(self.dispatch_callback_button)

    def handle_help(self, message: Message) -> None:
        """Обработка команды /help."""
        help_text: str = (
            "Доступные команды:\n"
        )
        self.bot.reply_to(
            message,
            help_text
        )

    def handle_start(self, message: Message) -> None:
        """Обработка команды /start."""
        is_new_user: bool = not self._is_user_exists(message.from_user)
        if is_new_user:
            created_user: UserDTO = self.user_repository.create_user(
                UserCreateDTO(
                    token=message.from_user.id,
                    username=message.from_user.username
                )
            )
            created_user = {"username": "esheloncr1"}
            return self.bot.send_message(
                message.chat.id,
                f"Добро пожаловать, {created_user['username']}",
                reply_markup=self.keyboard_markup.default_markup
            )
        self.bot.reply_to(
            message,
            "Неизвестная команда",
            reply_markup=self.keyboard_markup.default_markup
        )

    def dispatch_callback_button(self, callback_data: CallbackQuery) -> None:
        """Определяет, какая команда вызвана(кнопкой) и вызывает обработчик."""
        callback_name: str = callback_data.data
        method: Optional[Callable] = getattr(self, f"handle_{callback_name}", None)
        if not method:
            return logger.warning(f"Не найден обработчик для {callback_name}")
        return method(callback_data)

    def handle_create_wallet(self, callback_data: CallbackQuery) -> None:
        """Обработчик для создания кошелька."""
        self.bot.send_message(callback_data.message.chat.id, "Введите наименование кошелька")
        self.bot.register_next_step_handler(callback_data.message, self._process_create_wallet)
        self.bot.answer_callback_query(callback_data.id)

    def handle_list_wallet(self, callback_data: CallbackQuery) -> None:
        """Обработчик для списка кошельков."""
        wallet_list: list[WalletDTO] = self.wallet_repository.list_wallet(
            callback_data.from_user.username
        )
        wallet_list_str: str = (
            "Доступные кошельки:\n" + ", ".join([f"{wallet['name']} (ID - {wallet['id']})"  for wallet in wallet_list])
        )
        self.bot.send_message(
            callback_data.message.chat.id,
            wallet_list_str,
            reply_markup=self.keyboard_markup.default_markup
        )
        self.bot.answer_callback_query(callback_data.id)

    def handle_delete_wallet(self, callback_data: CallbackQuery) -> None:
        """Обработчик для удаления кошельков."""
        self.bot.send_message(callback_data.message.chat.id, "Введите ID кошелька.")
        self.bot.register_next_step_handler(callback_data.message, self._process_delete_wallet)
        self.bot.answer_callback_query(callback_data.id)

    def _process_delete_wallet(self, message: Message) -> None:
        """Удаление кошелька."""
        self.wallet_repository.delete_wallet(message.text)
        self.bot.send_message(
            message.chat.id,
            "Кошелёк успешно удалён",
            reply_markup=self.keyboard_markup.default_markup
        )

    def _process_create_wallet(self, message: Message) -> None:
        """Создание кошелька."""
        wallet: WalletDTO = self.wallet_repository.create_wallet(
            WalletCreateDTO(
                outer_owner_id=message.from_user.id,
                name=message.text,
            )
        )
        self.bot.send_message(
            message.chat.id,
            f"Кошелёк {wallet['name']} успешно создан.",
            reply_markup=self.keyboard_markup.default_markup
        )

    def _is_user_exists(self, user: User) -> bool:
        """Проверяет, существует ли пользователь в БД."""
        return self.user_repository.is_user_exists_by_token(user.id)
