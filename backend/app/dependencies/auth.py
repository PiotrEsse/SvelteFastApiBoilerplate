"""Authentication related dependencies."""

from fastapi import Depends, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.core.config import get_settings
from backend.app.models.user import User


class AuthenticationError(Exception):
    """Raised when authentication credentials are missing or invalid."""

    def __init__(self, detail: str, status_code: int = status.HTTP_401_UNAUTHORIZED) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def _get_token_from_request(request: Request, *, cookie_name: str) -> str | None:
    token = request.cookies.get(cookie_name)
    if token:
        return token
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ", 1)[1]
    return None


async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Validate the access token and load the corresponding user."""

    settings = get_settings()
    token = _get_token_from_request(
        request, cookie_name=settings.access_token_cookie_name
    )
    if not token:
        raise AuthenticationError("Not authenticated")

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_aud": False},
        )
    except JWTError as exc:  # pragma: no cover - defensive branch
        raise AuthenticationError("Could not validate credentials") from exc

    token_type = payload.get("type")
    if token_type != "access":
        raise AuthenticationError("Invalid token type")

    subject = payload.get("sub")
    if subject is None:
        raise AuthenticationError("Token subject missing")

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive branch
        raise AuthenticationError("Token subject invalid") from exc

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise AuthenticationError("User not found")

    request.state.user = user  # type: ignore[attr-defined]
    return user
