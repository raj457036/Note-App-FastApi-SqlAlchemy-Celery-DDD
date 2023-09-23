from abc import abstractmethod

from typing_extensions import override

from src.domain.common.use_case import AbstractUseCase
from src.domain.user.dtos import CreateUserDTO
from src.domain.user.models.entities.user import User


class CreateUserUsecase(AbstractUseCase[CreateUserDTO, User]):
    @override
    @abstractmethod
    def execute(self, dto: CreateUserDTO) -> User:
        raise NotImplementedError
