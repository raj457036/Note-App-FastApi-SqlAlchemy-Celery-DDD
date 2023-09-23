from typing_extensions import override

from src.domain.common.use_case import AbstractUseCase
from src.domain.notes.dtos import CreateNoteByFileDTO
from src.domain.notes.models.aggregates.note_upload import NoteUploadAggregate
from src.domain.notes.models.entities.notes import Note


class CreateNoteByFileUseCase(AbstractUseCase[CreateNoteByFileDTO, NoteUploadAggregate]):
    @override
    def execute(self, dto: CreateNoteByFileDTO) -> NoteUploadAggregate:
        raise NotImplementedError
