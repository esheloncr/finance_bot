import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as l_


class User(AbstractUser):
    outer_id = models.CharField(
        l_("ID пользователя во внешней системе."),
        max_length=255,
        blank=True,
    )


class Wallet(models.Model):
    """Кошелёк."""
    owner_id: int
    owner = models.ForeignKey(
        User,
        verbose_name=l_("Владелец"),
        on_delete=models.CASCADE,
        related_name="wallets"
    )
    name = models.CharField(
        l_("Наименование"),
        max_length=100,
    )
    is_active = models.BooleanField(
        l_("Активный"),
        default=False
    )

    class Meta:
        verbose_name = l_("Кошелёк")
        verbose_name_plural = l_("Кошельки")
        constraints = [
            models.UniqueConstraint(
                fields=["owner"],
                condition=models.Q(is_active=True),
                name="unique_active_wallet_per_user"
            )
        ]

    def __str__(self) -> str:
        return _(f"Кошелёк {self.name} пользователя {self.owner.username}")


class Transaction(models.Model):
    """Транзакция."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_id: int
    wallet = models.ForeignKey(
        Wallet,
        verbose_name=l_("Кошелёк"),
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    amount = models.DecimalField(
        l_("Значение"),
        decimal_places=2,
        max_digits=15,
    )
    reason = models.CharField(
        l_("Обоснование транзакции"),
        max_length=255,
        blank=True
    )
    created_at = models.DateTimeField(
        l_("Дата и время создания"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = l_("Транзакция")
        verbose_name_plural = l_("Транзакции")

    def __str__(self) -> str:
        return str(self.id)

    @property
    def has_reason(self) -> bool:
        """Проверяет указано ли обоснование."""
        return bool(self.reason)
