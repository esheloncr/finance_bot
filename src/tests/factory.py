import pytest

import factory

from factory import django
from factory import fuzzy

from src.models import Wallet, Transaction, User


pytestmark = [
    pytest.mark.django_db
]


class UserFactory(django.DjangoModelFactory):
    """Фабрика для создания пользователя."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test_user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    outer_id = fuzzy.FuzzyText()


class WalletFactory(django.DjangoModelFactory):
    """Фабрика для создания кошельков."""

    class Meta:
        model = Wallet

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker("text")


class TransactionFactory(django.DjangoModelFactory):
    """Фабрика для создания транзакций."""

    class Meta:
        model = Transaction

    wallet = factory.SubFactory(WalletFactory)
    amount = fuzzy.FuzzyDecimal(low=1)
    reason = fuzzy.FuzzyText()
