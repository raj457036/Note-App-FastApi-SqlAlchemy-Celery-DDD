from dataclasses import dataclass
from uuid import UUID


@dataclass(
    frozen=True
)
class CreateNoteDTO:
    title: str
    content: str
    user_id: UUID


@dataclass(
    frozen=True
)
class CreateNoteByFileDTO:
    title: str
    user_id: UUID
