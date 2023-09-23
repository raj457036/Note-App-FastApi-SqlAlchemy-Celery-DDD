from typing_extensions import override

from src.domain.common.use_case import AbstractUseCase
from src.domain.notes.dtos import CreateNoteDTO
from src.domain.notes.models.entities.notes import Note


class CreateNoteUseCase(AbstractUseCase[CreateNoteDTO, Note]):
    @override
    def execute(self, dto: CreateNoteDTO) -> Note:
        raise NotImplementedError
