"""Todo item model definition."""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from . import Base


class TodoStatus(str, Enum):
    """Enumeration of available todo item statuses."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoItem(Base):
    """Represents a todo item belonging to a user."""

    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SAEnum(TodoStatus, name="todo_status"),
        nullable=False,
        default=TodoStatus.PENDING,
        server_default=TodoStatus.PENDING.value,
        index=True,
    )
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now(),
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    owner = relationship("User", back_populates="todos")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"TodoItem(id={self.id!r}, title={self.title!r}, status={self.status!r})"
