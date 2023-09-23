from contextlib import contextmanager
from typing import Generator, Generic, TypeVar

from sqlalchemy.orm import Query, Session

from src.infra.database.connection import Database

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, database: Database, model: type[T]) -> None:
        super().__init__()
        self.model: type[T] = model
        self._database = database

    @contextmanager
    def query(self) -> Generator[Query[T], None, None]:
        with self._database.session() as session:
            yield session.query(self.model)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        with self._database.session() as session:
            yield session
