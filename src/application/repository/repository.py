from __future__ import annotations

from typing import TYPE_CHECKING

from src.models import Wallet, Transaction, User
from src.application.infrastructure.dto.dto import (
    TransactionDTO,
    WalletDTO
)
from src.application.infrastructure.dto.user import UserDTO, UserCreateDTO

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from src.application.infrastructure.dto.dto import (
        WalletCreateDTO,
        TransactionCreateDTO,
        TransactionFilterDTO,
    )


class UserRepository:
    """Репозиторий для работы с пользователями."""

    @classmethod
    def create_user(cls, user_create_data: UserCreateDTO) -> UserDTO:
        """Создание пользователя."""
        user: User = User(
            username=user_create_data["username"],
            outer_id=user_create_data["token"],
        )
        user.save()
        return UserDTO(
            id=user.id,
            token=user_create_data["token"],
            username=user.username
        )

    @classmethod
    def get_user_by_token(cls, token: str) -> UserDTO:
        """Получить пользователя по токену."""
        user: User = User.objects.get(outer_id=token)
        return UserDTO(
            id=user.id,
            token=user.outer_id,
            username=user.username,
        )

    @classmethod
    def is_user_exists_by_token(cls, token: str) -> bool:
        """Проверяет, существует ли пользователь по токену."""
        return User.objects.filter(outer_id=token).exists()


class WalletRepository:
    """DAO для кошельков."""

    @classmethod
    def get_wallet(cls, wallet_id: int) -> WalletDTO:
        """Получить информацию о кошельке."""
        wallet: Wallet = Wallet.objects.get(id=wallet_id)
        return WalletDTO(
            id=wallet.id,
            owner=UserDTO(
                id=wallet.owner.id,
                token="",
                username=wallet.owner.username,
            ),
            name=wallet.name,
        )

    @classmethod
    def create_wallet(cls, create_data: WalletCreateDTO) -> WalletDTO:
        """Создание кошелька."""
        if create_data.get("outer_owner_id"):
            create_data["owner_id"] = UserRepository.get_user_by_token(
                create_data.pop("outer_owner_id")
            )["id"]
        wallet: Wallet = Wallet.objects.create(**create_data)
        return WalletDTO(
            id=wallet.id,
            owner=UserDTO(
                id=wallet.owner.id,
                token=str(),
                username=wallet.owner.username,
            ),
            name=wallet.name
        )

    @classmethod
    def delete_wallet(cls, wallet_id: int) -> None:
        """Удаление кошелька."""
        Wallet.objects.filter(id=wallet_id).delete()

    @classmethod
    def list_wallet(cls, username: str) -> list[WalletDTO]:
        """Получить список кошельков."""
        queryset: QuerySet[Wallet] = Wallet.objects.filter(owner__username=username)
        return [
            WalletDTO(
                id=wallet.id,
                owner=UserDTO(
                    id=wallet.owner.id,
                    token=wallet.owner.outer_id,
                    username=wallet.owner.username
                ),
                name=wallet.name
            ) for wallet in queryset
        ]


class TransactionRepository:
    """Репозиторий для транзакций."""

    @classmethod
    def create_transaction(cls, create_data: TransactionCreateDTO) -> TransactionDTO:
        """Создание транзакции."""
        transaction: Transaction = Transaction.objects.create(
            **create_data
        )
        return TransactionDTO(
            id=transaction.id,
            wallet_id=transaction.wallet_id,
            amount=transaction.amount,
            reason=transaction.reason,
            created_at=transaction.created_at
        )

    @classmethod
    def get_transaction_list_by_wallet_id(
        cls,
        wallet_id: int,
        **filters: TransactionFilterDTO
    ) -> list[TransactionDTO]:
        """Получить список транзакций по ID кошелька."""
        queryset = Transaction.objects.filter(
            wallet_id=wallet_id,
            **filters
        )
        return [
            TransactionDTO(
                id=transaction.id,
                wallet_id=transaction.wallet_id,
                amount=transaction.amount,
                reason=transaction.reason,
                created_at=transaction.created_at
            ) for transaction in queryset 
        ]
