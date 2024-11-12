from typing import TypedDict


class UserDTO(TypedDict):
    """Описание пользователя."""
    id: int
    token: str
    username: str


class UserCreateDTO(TypedDict):
    """Схема для создания пользователя."""
    token: str
    username: str
