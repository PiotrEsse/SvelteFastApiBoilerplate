"""Schemas related to authentication flows."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Payload for user login."""

    email: EmailStr
    password: str


