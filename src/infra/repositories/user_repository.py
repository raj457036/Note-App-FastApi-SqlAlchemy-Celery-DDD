from uuid import UUID

from typing_extensions import override

from src.core.errors.base import ResourceNotFoundException
from src.domain.user.models.entities import User
from src.domain.user.repositories.user_repository import AbstractUserRepository
from src.infra.database.connection import Database
from src.infra.database.models.user import UserModel
from src.infra.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel], AbstractUserRepository):
    def __init__(self, database: Database):
        super().__init__(database=database, model=UserModel)

    @override
    def get(self, user_id: UUID) -> User:
        with self.query() as query:
            user = query.filter(
                UserModel.id == user_id).first()

        if not user:
            raise ResourceNotFoundException(User)

        return User.model_validate(user, from_attributes=True)

    @override
    def get_by_email(self, email: str) -> User:
        with self.query() as query:
            user = query.filter_by(email=email).first()
        return User.model_validate(user, from_attributes=True)

    @override
    def create(self, *, name: str, email: str, password: str) -> User:
        hash_password = User.hash_password(password)

        user = UserModel(
            name=name,
            email=email,
            password_hash=hash_password
        )
        with self.session() as session:
            session.add(user)
            session.commit()

            return User.model_validate(user, from_attributes=True)

    @override
    def update(self, user_id: UUID, *, name: str | None, email: str | None, password: str | None) -> User:
        _updates = {}
        if name:
            _updates["name"] = name
        if email:
            _updates["email"] = email
        if password:
            _updates["password_hash"] = User.hash_password(password)

        with self.query() as query:
            query.filter(UserModel.id == user_id)\
                .update(_updates)

        return self.get(user_id)

    @override
    def delete(self, user_id: UUID) -> None:
        with self.query() as query:
            query.filter(UserModel.id == user_id).delete()
