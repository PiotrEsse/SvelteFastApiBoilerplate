"""Pydantic schemas for user resources."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Shared user attributes."""

    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    """Schema used when creating a new user."""

    password: str


class UserRead(UserBase):
    """Schema returned when reading user data."""

    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """Schema used when updating a user."""

    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
