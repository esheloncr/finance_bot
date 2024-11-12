from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from factory import fuzzy

from src.tests.factory import (
    UserFactory,
    WalletFactory,
    TransactionFactory,
)

if TYPE_CHECKING:
    from src.models import Transaction, Wallet, User


@pytest.fixture()
def user() -> User:
    """Создаёт пользователя."""
    return UserFactory()


@pytest.fixture()
def wallet() -> Wallet:
    """Создаёт кошелёк."""
    return WalletFactory()


@pytest.fixture()
def transaction() -> Transaction:
    """Создаёт транзакцию."""
    return TransactionFactory()


@pytest.fixture()
def wallet_creation_data(user: User) -> dict:
    """Данные для создания кошелька."""
    return {
        "owner_id": user.id,
        "name": fuzzy.FuzzyText()
    }


@pytest.fixture()
def transaction_creation_data(wallet: Wallet) -> dict:
    """Данные для создания транзакции."""
    return {
        "wallet_id": wallet.id,
        "amount": fuzzy.FuzzyDecimal(low=1).fuzz(),
        "reason": fuzzy.FuzzyText()
    }
