from typing_extensions import override

from src.domain.notes.dtos import CreateNoteByFileDTO
from src.domain.notes.models.aggregates.note_upload import NoteUploadAggregate
from src.domain.notes.services.note_service import AbstractNoteService
from src.domain.notes.usecases.create_note_by_file import \
    CreateNoteByFileUseCase


class CreateNoteByFileUseCaseImpl(CreateNoteByFileUseCase):

    def __init__(self, service: AbstractNoteService) -> None:
        super().__init__()
        self._service = service

    @override
    def execute(self, dto: CreateNoteByFileDTO) -> NoteUploadAggregate:
        return self._service.create_note_by_file(
            title=dto.title,
            user_id=dto.user_id,
        )
