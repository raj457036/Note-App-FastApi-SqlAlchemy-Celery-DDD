import logging
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.di.injector import RootContainer
from src.domain.user.dtos import CreateUserDTO
from src.domain.user.models.entities.user import User
from src.domain.user.usecases.create_user import CreateUserUsecase
from src.domain.user.usecases.get_user_by_id import GetUserByIdUseCase

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users")


@router.post("/", response_model=User)
@inject
def create_user(
    dto: CreateUserDTO,
    create_user: CreateUserUsecase = Depends(
        Provide[RootContainer.user.create_user]),
):
    logger.info(f"Creating user {dto}")
    user = create_user.execute(dto)
    return user


@router.get(
    "/{user_id}",
    response_model=User,
)
@inject
def get_user(
        user_id: UUID,
        get_user: GetUserByIdUseCase = Depends(
            Provide[RootContainer.user.get_user_by_id]),
):
    logger.info(f"Getting user {user_id}")
    # time.sleep(0.4)
    user = get_user.execute(user_id)
    return user
