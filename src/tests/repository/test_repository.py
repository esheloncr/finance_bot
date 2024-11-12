import pytest

from decimal import Decimal

from src.models import Wallet
from src.application.infrastructure.dto.dto import (
    WalletDTO,
    TransactionDTO,
    TransactionFilterDTO,
)
from src.application.repository.repository import (
    WalletRepository,
    TransactionRepository,
)


@pytest.mark.django_db
class TestWalletRepository:
    """Тестирование функционала WalletRepository."""
    repository: WalletRepository = WalletRepository

    def test_get_wallet(self, wallet: Wallet) -> None:
        """Тестирует получение информации о кошельке."""
        wallet: WalletDTO = self.repository.get_wallet(wallet.id)
        assert wallet
        assert wallet["owner"]
        assert wallet["name"]

    def test_create_wallet(self, wallet_creation_data: dict) -> None:
        """Тестирует создание кошелька."""
        wallet: WalletDTO = self.repository.create_wallet(wallet_creation_data)
        assert wallet
        assert wallet["owner"]
        assert wallet["name"] == wallet_creation_data["name"]

    def test_delete_wallet(self, wallet: Wallet) -> None:
        """Тестирует удаление кошелька."""
        wallet_id: int = wallet.id
        assert Wallet.objects.filter(pk=wallet_id).exists()
        self.repository.delete_wallet(wallet_id)
        assert not Wallet.objects.filter(pk=wallet_id).exists()


@pytest.mark.django_db
class TestTransactionRepository:
    """Тестирование функционала TransactionRepository."""

    repository: TransactionRepository = TransactionRepository

    def test_create_transaction(self, transaction_creation_data: dict) -> None:
        """Тестирование создания транзакции."""
        transaction: TransactionDTO = self.repository.create_transaction(
            transaction_creation_data
        )
        assert transaction
        assert transaction["wallet_id"] == transaction_creation_data["wallet_id"]
        assert transaction["amount"] == transaction_creation_data["amount"]

    def test_get_transaction_list(self, wallet: Wallet) -> None:
        """Тестирование списка транзакций."""
        transaction_data: dict = {
            "wallet_id": wallet.id,
            "amount": Decimal("5.00"),
            "reason": "test"
        }
        created_transaction: TransactionDTO = self.repository.create_transaction(transaction_data)
        wrong_filters: TransactionFilterDTO = TransactionFilterDTO(
            amount__gte=created_transaction["amount"],
            reason__isnull=True,
        )
        empty_filters: TransactionFilterDTO = TransactionFilterDTO()
        success_filters: TransactionFilterDTO = TransactionFilterDTO(
            amount__lte=Decimal("10"),
            reason__isnull=False
        )
        assert not len(self.repository.get_transaction_list_by_wallet_id(wallet.id, **wrong_filters))
        assert len(self.repository.get_transaction_list_by_wallet_id(wallet.id, **empty_filters))
        assert len(self.repository.get_transaction_list_by_wallet_id(wallet.id, **success_filters))
