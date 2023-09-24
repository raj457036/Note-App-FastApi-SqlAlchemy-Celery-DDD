from dependency_injector import containers, providers

from src.core.di.note_container import NoteContainer
from src.core.di.user_container import UserContainer
from src.infra.common.integration.sns_setup import SNSSetupFactory
from src.infra.common.integration.storage.s3_storage_provider import \
    S3StorageProvider
from src.infra.database.connection import Database


class RootContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # database
    database = providers.Singleton(Database)

    # integrations
    file_storage_provider = providers.Factory(
        S3StorageProvider,
        endpoint=config.s3_endpoint.as_(str),
        bucket_name=config.s3_bucket_name.as_(str),
    )

    sns_provider = providers.Singleton(
        SNSSetupFactory,
        s3_endpoint=config.s3_endpoint.as_(str),
        sns_endpoint=config.sns_endpoint.as_(str),
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
