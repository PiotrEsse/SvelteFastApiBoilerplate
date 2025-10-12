"""Common dependencies used across API routers."""

from typing import Generator

from sqlalchemy.orm import Session

from backend.app.db.session import get_session


def get_db() -> Generator[Session, None, None]:
    """Expose the SQLAlchemy session as a dependency."""

    yield from get_session()
