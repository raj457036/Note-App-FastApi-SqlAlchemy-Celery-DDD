from dependency_injector import containers, providers

from src.app.services.user_service import UserServiceImpl
from src.app.usecases.user import (CreateUserUseCaseImpl,
                                   DeleteUserByIdUseCaseImpl,
                                   GetUserByIdUseCaseImpl,
                                   UpdateUserUseCaseImpl)
from src.domain.user.repositories import AbstractUserRepository
from src.domain.user.services import AbstractUserService
from src.domain.user.usecases import (CreateUserUsecase, DeleteUserByIdUseCase,
                                      GetUserByIdUseCase, UpdateUserUseCase)
from src.infra.database.connection import Database, connection_url
from src.infra.repositories.user_repository import UserRepository


class UserContainer(containers.DeclarativeContainer):
    # database
    database = providers.Dependency(Database)

    # repositories
    user_repository: providers.Factory[AbstractUserRepository] = providers.Factory(
        UserRepository,
        database=database,
    )

    # services
    user_service: providers.Factory[AbstractUserService] = providers.Factory(
        UserServiceImpl,
        user_repository=user_repository,
    )

    # usecases
    get_user_by_id: providers.Factory[GetUserByIdUseCase] = providers.Factory(
        GetUserByIdUseCaseImpl,
        service=user_service,
    )

    create_user: providers.Factory[CreateUserUsecase] = providers.Factory(
        CreateUserUseCaseImpl,
        service=user_service,
    )

    update_user: providers.Factory[UpdateUserUseCase] = providers.Factory(
        UpdateUserUseCaseImpl,
        service=user_service,
    )

    delete_user_by_id: providers.Factory[DeleteUserByIdUseCase] = providers.Factory(
        DeleteUserByIdUseCaseImpl,
        service=user_service,
    )
