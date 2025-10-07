"""Common dependencies used across API routers."""

from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_session
from backend.app.models.user import User


def get_db() -> Generator[Session, None, None]:
    """Expose the SQLAlchemy session as a dependency."""

    yield from get_session()


async def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> User:
    """Simple dependency that extracts the current user from headers."""

    user_id_header = request.headers.get("X-User-Id")
    if not user_id_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    try:
        user_id = int(user_id_header)
    except ValueError as exc:  # pragma: no cover - defensive programming
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user identifier",
        ) from exc

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
