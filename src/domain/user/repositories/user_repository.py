from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user.models.entities.user import User


class AbstractUserRepository(ABC):

    @abstractmethod
    def get(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def create(self, *, name: str, email: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: UUID, *, name: str | None, email: str | None, password: str | None) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        raise NotImplementedError
