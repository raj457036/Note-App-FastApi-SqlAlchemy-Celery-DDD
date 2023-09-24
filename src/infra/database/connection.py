import logging
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (DeclarativeBase, Session, scoped_session,
                            sessionmaker)

from src.core.settings import Settings

logger = logging.getLogger(__name__)

setting = Settings.cached()
connection_url = "postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}".format_map({
    "PG_USER": setting.pg_user,
    "PG_PASSWORD": setting.pg_password.get_secret_value(),
    "PG_HOST": setting.pg_host,
    "PG_DB": setting.pg_db
})


class BaseDBModel(DeclarativeBase):
    pass


class Database:
    def __init__(self, *, connection_url: str = connection_url) -> None:
        self.engine = create_engine(connection_url, echo=True)

    def _session_factory(self) -> Session:
        _S = scoped_session(
            sessionmaker(
                self.engine,
                autoflush=True,
            )
        )
        return _S()

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
