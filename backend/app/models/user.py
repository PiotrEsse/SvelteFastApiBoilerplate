"""User model definition."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import expression, func
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    """Represents an application user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default=expression.true(),
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
        index=True,
    )

    todos = relationship(
        "TodoItem",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"User(id={self.id!r}, email={self.email!r})"
