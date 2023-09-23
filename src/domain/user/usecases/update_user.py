from abc import abstractmethod

from typing_extensions import override

from src.domain.common.use_case import AbstractUseCase
from src.domain.user.dtos import UpdateUserDTO
from src.domain.user.models.entities.user import User


class UpdateUserUseCase(AbstractUseCase[UpdateUserDTO, User]):
    @override
    @abstractmethod
    def execute(self, dto: UpdateUserDTO) -> User:
        raise NotImplementedError
