from typing_extensions import override

from src.domain.user.dtos import CreateUserDTO
from src.domain.user.models.entities.user import User
from src.domain.user.services.user_service import AbstractUserService
from src.domain.user.usecases import CreateUserUsecase


class CreateUserUseCaseImpl(CreateUserUsecase):
    def __init__(self, service: AbstractUserService) -> None:
        self.service = service

    @override
    def execute(self, dto: CreateUserDTO) -> User:
        return self.service.create_user(
            name=dto.name,
            email=dto.email,
            password=dto.password,
        )
