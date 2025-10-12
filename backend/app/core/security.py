"""Security helpers for password hashing and JWT token generation."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import jwt
from passlib.context import CryptContext

from backend.app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return whether the provided password matches the stored hash."""

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash the provided password using a secure algorithm."""

    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, int],
    *,
    expires_delta: Optional[timedelta] = None,
    token_type: str = "access",
    additional_claims: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate a signed JWT access or refresh token for the given subject."""

    settings = get_settings()
    now = datetime.utcnow()
    if expires_delta is None:
        if token_type == "refresh":
            expires_delta = timedelta(days=settings.refresh_token_expire_days)
        else:
            expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = now + expires_delta
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": token_type,
    }
    if additional_claims:
        to_encode.update(additional_claims)
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
