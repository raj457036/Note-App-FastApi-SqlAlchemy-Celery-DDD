from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.notes.models.aggregates.note_upload import NoteUploadAggregate
from src.domain.notes.models.entities.notes import Note


class AbstractNoteService(ABC):

    @abstractmethod
    def get_note_by_id(self, note_id: UUID) -> Note:
        raise NotImplementedError

    @abstractmethod
    def create_note(self, title: str, content: str, user_id: UUID) -> Note:
        raise NotImplementedError

    @abstractmethod
    def create_note_by_file(self, title: str, user_id: UUID) -> NoteUploadAggregate:
        raise NotImplementedError
