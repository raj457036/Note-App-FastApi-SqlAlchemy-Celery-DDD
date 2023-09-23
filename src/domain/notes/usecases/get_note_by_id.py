from uuid import UUID

from typing_extensions import override

from src.domain.common.use_case import AbstractUseCase
from src.domain.notes.models.entities.notes import Note


class GetNoteByIDUseCase(AbstractUseCase[UUID, Note]):
    @override
    def execute(self, dto: UUID) -> Note:
        raise NotImplementedError
