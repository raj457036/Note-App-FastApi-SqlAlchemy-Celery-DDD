from dependency_injector import containers, providers

from src.app.services.note_service import NoteServiceImpl
from src.app.usecases.note.create_note import CreateNoteUseCaseImpl
from src.app.usecases.note.create_note_by_file import \
    CreateNoteByFileUseCaseImpl
from src.app.usecases.note.get_note_by_id import GetNoteByIDUseCaseImpl
from src.domain.integration.storage import FileStorageService
from src.infra.database.connection import Database
from src.infra.repositories.note_repository import NoteRepositoryImpl


class NoteContainer(containers.DeclarativeContainer):

    # database
    database = providers.Dependency(Database)

    # integration
    storage_service = providers.Dependency(FileStorageService)

    # repositories
    note_repository = providers.Factory(
        NoteRepositoryImpl,
        database=database,
    )

    # services
    note_service = providers.Factory(
        NoteServiceImpl,
        repository=note_repository,
        storage_service=storage_service,
    )

    # usecases
    get_note_by_id = providers.Factory(
        GetNoteByIDUseCaseImpl,
        service=note_service,
    )

    create_note = providers.Factory(
        CreateNoteUseCaseImpl,
        service=note_service,
    )

    create_note_by_file = providers.Factory(
        CreateNoteByFileUseCaseImpl,
        service=note_service,

    )
