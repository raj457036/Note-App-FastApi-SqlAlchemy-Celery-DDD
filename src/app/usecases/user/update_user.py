from typing_extensions import override

from src.domain.user.dtos import UpdateUserDTO
from src.domain.user.models.entities.user import User
from src.domain.user.services.user_service import AbstractUserService
from src.domain.user.usecases import UpdateUserUseCase


class UpdateUserUseCaseImpl(UpdateUserUseCase):
    def __init__(self, service: AbstractUserService) -> None:
        self.service = service

    @override
    def execute(self, dto: UpdateUserDTO) -> User:
        return self.service.update_user(
            user_id=dto.user_id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
        )
