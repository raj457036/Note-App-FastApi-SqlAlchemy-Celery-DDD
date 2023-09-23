from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user.models.entities.user import UUID, User


class AbstractUserService(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, *, name: str, email: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user_id: UUID, *, name: str | None, email: str | None, password: str | None) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete_user_by_id(self, user_id: UUID) -> None:
        raise NotImplementedError
