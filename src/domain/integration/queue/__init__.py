from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

MessageFormat = TypeVar('MessageFormat', bound=BaseModel)


class MessageQueueService(Generic[MessageFormat], ABC):

    @abstractmethod
    def get_messages(self, **kwargs) -> list[MessageFormat]:
        raise NotImplementedError

    @abstractmethod
    def delete_message(self, **kwargs) -> None:
        raise NotImplementedError
