from uuid import UUID

from typing_extensions import override

from src.domain.notes.models.entities.notes import Note
from src.domain.notes.services.note_service import AbstractNoteService
from src.domain.notes.usecases.get_note_by_id import GetNoteByIDUseCase


class GetNoteByIDUseCaseImpl(GetNoteByIDUseCase):
    def __init__(self, service: AbstractNoteService) -> None:
        super().__init__()
        self._service = service

    @override
    def execute(self, note_id: UUID) -> Note:
        return self._service.get_note_by_id(note_id)
