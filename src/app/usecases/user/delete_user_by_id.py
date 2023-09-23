from uuid import UUID

from typing_extensions import override

from src.domain.user.services.user_service import AbstractUserService
from src.domain.user.usecases import DeleteUserByIdUseCase


class DeleteUserByIdUseCaseImpl(DeleteUserByIdUseCase):
    def __init__(self, *, service: AbstractUserService) -> None:
        self.service = service

    @override
    def execute(self, user_id: UUID) -> None:
        return self.service.delete_user_by_id(user_id)
