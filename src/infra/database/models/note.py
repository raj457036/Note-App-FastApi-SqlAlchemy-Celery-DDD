from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.connection import BaseDBModel

if TYPE_CHECKING:
    from src.infra.database.models.user import UserModel


class NoteModel(BaseDBModel):
    __tablename__ = 'notes'

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    file_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    with_file: Mapped[bool] = mapped_column(Boolean, default=False)
    file_processing_status: Mapped[str] = mapped_column(
        Enum(
            'pending',
            'scheduled',
            'processing',
            'processed',
            'failed',
            name='note_file_processing_status'
        ),
        nullable=True
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="notes")
