from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CreateUserDTO:
    name: str
    email: str
    password: str


@dataclass(frozen=True)
class UpdateUserDTO:
    user_id: UUID
    name: str | None
    email: str | None
    password: str | None
