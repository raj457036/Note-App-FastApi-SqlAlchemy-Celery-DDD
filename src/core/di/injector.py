from dependency_injector import containers, providers

from src.core.di.note_container import NoteContainer
from src.core.di.user_container import UserContainer
from src.infra.database.connection import Database, connection_url


class RootContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # database
    database = providers.Singleton(
        Database,
        connection_url=connection_url,
    )

    # containers
    user: providers.Container[UserContainer] = providers.Container(
        UserContainer,
        database=database,
    )

    note: providers.Container[NoteContainer] = providers.Container(
        NoteContainer,
        database=database,
    )
