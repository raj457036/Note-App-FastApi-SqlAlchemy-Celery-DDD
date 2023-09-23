from uuid import UUID

from typing_extensions import override

from src.domain.user.models.entities.user import User
from src.domain.user.repositories.user_repository import AbstractUserRepository
from src.domain.user.services.user_service import AbstractUserService


class UserServiceImpl(AbstractUserService):
    def __init__(
        self,
        *,
        user_repository: AbstractUserRepository,
    ) -> None:
        self.repository = user_repository

    @override
    def get_user_by_id(self, user_id: UUID) -> User:
        return self.repository.get(user_id)

    @override
    def get_user_by_email(self, email: str) -> User:
        return self.repository.get_by_email(email)

    @override
    def create_user(self, *, name: str, email: str, password: str) -> User:
        return self.repository.create(name=name, email=email, password=password)

    @override
    def update_user(self, user_id: UUID, *, name: str | None, email: str | None, password: str | None) -> User:
        return self.repository.update(user_id, name=name, email=email, password=password)

    @override
    def delete_user_by_id(self, user_id: UUID) -> None:
        return self.repository.delete(user_id)
