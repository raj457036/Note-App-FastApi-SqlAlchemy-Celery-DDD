from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DTO = TypeVar("DTO")
ReturnType = TypeVar("ReturnType")


class AbstractUseCase(Generic[DTO, ReturnType], ABC):
    @abstractmethod
    def execute(self, param: DTO) -> ReturnType:
        raise NotImplementedError
