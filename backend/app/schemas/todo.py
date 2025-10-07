"""Pydantic schemas for todo resources."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.app.models.todo import TodoStatus


class TodoBase(BaseModel):
    """Shared attributes for todo items."""

    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.PENDING
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    """Schema for creating a todo item."""

    pass


class TodoUpdate(BaseModel):
    """Schema for updating a todo item."""

    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[TodoStatus] = None
    due_date: Optional[datetime] = None


class TodoRead(TodoBase):
    """Schema returned when reading todo items."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
