"""Authentication API router."""

import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.core.config import get_settings
from backend.app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest
from backend.app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


def _cookie_options(*, http_only: bool) -> dict:
    settings = get_settings()
    options = {
        "httponly": http_only,
        "secure": settings.cookie_secure,
        "samesite": settings.cookie_samesite,
        "path": "/",
    }
    if settings.cookie_domain:
        options["domain"] = settings.cookie_domain
    return options


def _issue_tokens(user: User) -> tuple[str, str, int, int]:
    settings = get_settings()
    access_delta = timedelta(minutes=settings.access_token_expire_minutes)
    refresh_delta = timedelta(days=settings.refresh_token_expire_days)
    access_token = create_access_token(user.id, expires_delta=access_delta)
    refresh_token = create_access_token(
        user.id, expires_delta=refresh_delta, token_type="refresh"
    )
    return (
        access_token,
        refresh_token,
        int(access_delta.total_seconds()),
        int(refresh_delta.total_seconds()),
    )


def _set_auth_cookies(
    response: Response,
    *,
    access_token: str,
    refresh_token: str,
    access_max_age: int,
    refresh_max_age: int,
) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.access_token_cookie_name,
        value=access_token,
        max_age=access_max_age,
        **_cookie_options(http_only=True),
    )
    response.set_cookie(
        key=settings.refresh_token_cookie_name,
        value=refresh_token,
        max_age=refresh_max_age,
        **_cookie_options(http_only=True),
    )
    csrf_token = secrets.token_urlsafe(32)
    response.set_cookie(
        key=settings.csrf_cookie_name,
        value=csrf_token,
        max_age=refresh_max_age,
        **_cookie_options(http_only=False),
    )
    response.headers[settings.csrf_header_name] = csrf_token
    expose_headers = response.headers.get("Access-Control-Expose-Headers")
    if expose_headers:
        if settings.csrf_header_name not in expose_headers:
            response.headers["Access-Control-Expose-Headers"] = \
                f"{expose_headers}, {settings.csrf_header_name}"
    else:
        response.headers["Access-Control-Expose-Headers"] = settings.csrf_header_name


def _clear_auth_cookies(response: Response) -> None:
    settings = get_settings()
    delete_kwargs: dict[str, str] = {"path": "/"}
    if settings.cookie_domain:
        delete_kwargs["domain"] = settings.cookie_domain
    response.delete_cookie(settings.access_token_cookie_name, **delete_kwargs)
    response.delete_cookie(settings.refresh_token_cookie_name, **delete_kwargs)
    response.delete_cookie(settings.csrf_cookie_name, **delete_kwargs)


def _get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    *, user_in: UserCreate, response: Response, db: Session = Depends(get_db)
) -> User:
    """Create a new user and issue authentication cookies."""

    existing_user = _get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token, refresh_token, access_max_age, refresh_max_age = _issue_tokens(user)
    _set_auth_cookies(
        response,
        access_token=access_token,
        refresh_token=refresh_token,
        access_max_age=access_max_age,
        refresh_max_age=refresh_max_age,
    )
    return user


@router.post("/login", response_model=UserRead)
def login_user(
    *, credentials: LoginRequest, response: Response, db: Session = Depends(get_db)
) -> User:
    """Authenticate a user using email and password."""

    user = _get_user_by_email(db, credentials.email)
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    access_token, refresh_token, access_max_age, refresh_max_age = _issue_tokens(user)
    _set_auth_cookies(
        response,
        access_token=access_token,
        refresh_token=refresh_token,
        access_max_age=access_max_age,
        refresh_max_age=refresh_max_age,
    )
    return user


@router.post("/refresh", response_model=UserRead)
def refresh_session(
    *, request: Request, response: Response, db: Session = Depends(get_db)
) -> User:
    """Issue a new access token using the refresh token cookie."""

    settings = get_settings()
    refresh_token = request.cookies.get(settings.refresh_token_cookie_name)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_aud": False},
        )
    except JWTError as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    subject = payload.get("sub")
    if subject is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject") from exc

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token, new_refresh_token, access_max_age, refresh_max_age = _issue_tokens(user)
    _set_auth_cookies(
        response,
        access_token=access_token,
        refresh_token=new_refresh_token,
        access_max_age=access_max_age,
        refresh_max_age=refresh_max_age,
    )
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    *, response: Response, current_user: User = Depends(get_current_user)
) -> None:
    """Clear authentication cookies to log the user out."""

    _ = current_user
    _clear_auth_cookies(response)
