from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class NoteFileProcessingStatus(Enum):
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Note(BaseModel):
    id: UUID
    title: str
    content: str
    user_id: UUID
    created_at: datetime
    file_path: str | None
    with_file: bool = False
    file_processing_status: NoteFileProcessingStatus | None = None

    class Config:
        from_attributes = True
        json_encoders = {
            UUID: lambda uuid: str(uuid)
        }
