from typing_extensions import override

from src.domain.notes.dtos import CreateNoteDTO
from src.domain.notes.models.entities.notes import Note
from src.domain.notes.services.note_service import AbstractNoteService
from src.domain.notes.usecases.create_note import CreateNoteUseCase


class CreateNoteUseCaseImpl(CreateNoteUseCase):

    def __init__(self, service: AbstractNoteService) -> None:
        self._service = service

    @override
    def execute(self, dto: CreateNoteDTO) -> Note:
        return self._service.create_note(
            title=dto.title,
            content=dto.content,
            user_id=dto.user_id,
        )
