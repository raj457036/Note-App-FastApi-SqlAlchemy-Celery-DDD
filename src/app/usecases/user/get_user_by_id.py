from uuid import UUID

from typing_extensions import override

from src.domain.user.models.entities.user import User
from src.domain.user.services.user_service import AbstractUserService
from src.domain.user.usecases.get_user_by_id import GetUserByIdUseCase


class GetUserByIdUseCaseImpl(GetUserByIdUseCase):
    def __init__(self, *, service: AbstractUserService) -> None:
        self.service = service

    @override
    def execute(self, user_id: UUID) -> User:
        try:
            return self.service.get_user_by_id(user_id=user_id)
        except Exception as e:
            raise e
