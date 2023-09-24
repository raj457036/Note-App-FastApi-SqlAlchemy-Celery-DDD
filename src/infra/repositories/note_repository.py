from uuid import UUID

from typing_extensions import override

from src.core.errors.base import ResourceNotFoundException
from src.domain.notes.models.entities.notes import Note
from src.domain.notes.repositories.note_repository import \
    AbstractNoteRepository
from src.infra.database.connection import Database
from src.infra.database.models.note import NoteModel
from src.infra.repositories.base_repository import BaseRepository


class NoteRepositoryImpl(BaseRepository[NoteModel], AbstractNoteRepository):
    def __init__(self, database: Database) -> None:
        super().__init__(database, NoteModel)

    @override
    def get_note_by_id(self, note_id: UUID) -> Note:
        with self.query() as query:
            note = query.filter(NoteModel.id == note_id).first()

        if not note:
            raise ResourceNotFoundException(Note)

        return Note.model_validate(note, from_attributes=True)

    @override
    def create_note(
        self, title: str, content: str, user_id: UUID, **kwargs
    ) -> Note:
        note = NoteModel(title=title, content=content,
                         user_id=user_id, **kwargs)

        with self.session() as session:
            session.add(note)
            session.commit()
            return Note.model_validate(note, from_attributes=True)
