from abc import abstractmethod
from uuid import UUID

from typing_extensions import override

from src.domain.common.use_case import AbstractUseCase
from src.domain.user.models.entities.user import User


class DeleteUserByIdUseCase(AbstractUseCase[UUID, User]):
    @override
    @abstractmethod
    def execute(self, param: UUID) -> None:
        raise NotImplementedError
