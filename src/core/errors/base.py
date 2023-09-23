from typing import Generic, TypeVar

ResourceType = TypeVar("ResourceType")


class DomainException(Exception):
    message: str = "An error occurred"
    code: str = "base_error"

    def __init__(self, *, message: str | None, code: str | None) -> None:
        self.message = message or self.message
        self.code = code or self.code
        super().__init__(self.message)


class ResourceNotFoundException(DomainException, Generic[ResourceType]):
    code: str = "resource_not_found"

    def __init__(self, resource: type[ResourceType], *, message: str | None = None, code: str | None = None) -> None:
        message = message or f"{resource.__name__} not found."
        code = code or self.code

        super().__init__(
            message=message,
            code=code
        )
