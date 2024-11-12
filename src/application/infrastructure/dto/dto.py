from __future__ import annotations

from typing import Optional, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from decimal import Decimal

    from src.application.infrastructure.dto.user import UserDTO


class TransactionDTO(TypedDict):
    """Описание транзакции."""
    id: str
    wallet_id: int
    amount: Decimal
    reason: Optional[str]
    created_at: str


class TransactionCreateDTO(TypedDict):
    """Описание схемы для создания транзакций."""
    wallet_id: int
    amount: Decimal
    reason: Optional[str]


class TransactionFilterDTO(TypedDict):
    """Фильтры для транзакций."""
    amount__gte: Optional[int]
    amount__lte: Optional[int]
    reason__isnull: Optional[bool]
    created_at__gte: Optional[str]
    created_at__lte: Optional[str]


class WalletDTO(TypedDict):
    """Описание кошелька."""
    id: int
    owner: UserDTO
    name: str


class WalletCreateDTO(TypedDict):
    """Схема данных для создания кошелька."""
    owner_id: Optional[int]
    outer_owner_id: Optional[int]
    name: str
