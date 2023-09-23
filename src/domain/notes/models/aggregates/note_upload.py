from pydantic import BaseModel

from src.domain.notes.models.entities.notes import Note
from src.domain.notes.models.value_objects.presigned_url_for_upload import \
    PresignedURLForUploadVO


class NoteUploadAggregate(BaseModel):
    note: Note
    presigned_url: PresignedURLForUploadVO
