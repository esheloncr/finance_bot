from telebot import types


class KeyboardMarkup:
    """Разметка меню для бота."""

    DEFAULT_BUTTONS: list[str] = [
        "create_wallet_button",
        "list_wallet_button",
        "delete_wallet",
    ]

    @property
    def default_markup(self) -> types.InlineKeyboardMarkup:
        """Получить стандартную разметку клавиатуры."""
        markup = types.InlineKeyboardMarkup()
        for button_name in self.DEFAULT_BUTTONS:
            markup.add(
                getattr(self, button_name)
            )
        return markup

    @property
    def create_wallet_button(self) -> types.InlineKeyboardButton:
        """Кнопка создания кошелька."""
        return types.InlineKeyboardButton(
            "Создать кошелёк",
            callback_data="create_wallet"
        )

    @property
    def list_wallet_button(self) -> types.InlineKeyboardButton:
        """Кнопка списка кошельков."""
        return types.InlineKeyboardButton(
            "Список кошельков",
            callback_data="list_wallet"
        )

    @property
    def delete_wallet(self) -> types.InlineKeyboardButton:
        """Кнопка удаления кошельков."""
        return types.InlineKeyboardButton(
            "Удалить кошелёк",
            callback_data="delete_wallet"
        )
