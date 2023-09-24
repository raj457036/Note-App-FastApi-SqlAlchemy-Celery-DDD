from dependency_injector import containers, providers

from src.core.di.note_container import NoteContainer
from src.core.di.user_container import UserContainer
from src.infra.database.connection import Database
from src.infra.integration.storage.s3 import S3FileStorageService


class RootContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # database
    database = providers.Singleton(Database)

    # integrations
    storage_service = providers.Factory(
        S3FileStorageService,
        endpoint=config.s3_endpoint.as_(str),
        bucket_name=config.s3_bucket_name.as_(str),
    )

    # containers
    user: providers.Container[UserContainer] = providers.Container(
        UserContainer,
        database=database,
    )

    note: providers.Container[NoteContainer] = providers.Container(
        NoteContainer,
        database=database,
        storage_service=storage_service,
    )
