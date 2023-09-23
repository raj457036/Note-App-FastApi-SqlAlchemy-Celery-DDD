from uuid import UUID

from typing_extensions import override

from src.domain.notes.models.aggregates.note_upload import NoteUploadAggregate
from src.domain.notes.models.entities.notes import Note
from src.domain.notes.repositories.note_repository import \
    AbstractNoteRepository
from src.domain.notes.services.note_service import AbstractNoteService


class NoteServiceImpl(AbstractNoteService):

    def __init__(self, repository: AbstractNoteRepository) -> None:
        self._repository = repository

    @override
    def get_note_by_id(self, note_id: UUID) -> Note:
        return self._repository.get_note_by_id(note_id)

    @override
    def create_note(
        self, title: str, content: str, user_id: UUID
    ) -> Note:
        return self._repository.create_note(
            title=title, content=content, user_id=user_id
        )

    @override
    def create_note_by_file(self, title: str, user_id: UUID) -> NoteUploadAggregate:
        raise NotImplementedError
