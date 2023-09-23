from typing import TYPE_CHECKING, List
from uuid import UUID, uuid4

from sqlalchemy import Boolean, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..connection import BaseDBModel

if TYPE_CHECKING:
    from src.infra.database.models.note import NoteModel


class UserModel(BaseDBModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True,
                                     default=uuid4)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[List["NoteModel"]] = relationship(
        "NoteModel", back_populates="user")

    def __str__(self) -> str:
        return f"UserModel(id={self.id}, name={self.name}, email={self.email})"
