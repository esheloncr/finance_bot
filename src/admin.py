from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as l_

from src.models import Wallet, Transaction, User


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """Админ класс для управления кошельками."""
    list_display: list[str] = [
        "name",
        "owner_username"
    ]

    @admin.display(description=l_("Владелец"))
    def owner_username(self, obj: Wallet) -> str:
        """Получить Username владельца кошелька."""
        return obj.owner.username


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админ класс для просмотра транзакций."""
    list_display: list[str] = [
        "id",
        "wallet",
        "amount",
        "has_reason",
    ]
    sortable_by: list[str] = [
        "amount",
    ]

    @admin.display(description=l_("Обоснован"))
    def has_reason(self, obj: Transaction) -> bool:
        return obj.has_reason

    def has_add_permission(
        self,
        request: HttpRequest
    ) -> bool:
        return True  # TODO: dev True

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj=...
    ) -> bool:
        return True  # TODO: dev True

    def has_change_permission(
        self,
        request: HttpRequest,
        obj=...
    ) -> bool:
        return True  # TODO: dev True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ класс для работы с пользователями."""
    list_display = BaseUserAdmin.list_display + ("outer_id", )
