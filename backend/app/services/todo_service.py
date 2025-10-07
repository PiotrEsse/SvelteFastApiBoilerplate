"""Business logic for todo operations."""

from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.todo import TodoItem, TodoStatus
from backend.app.schemas.todo import TodoCreate, TodoUpdate

TodoSchema = Union[TodoCreate, TodoUpdate]


def _model_to_dict(model: TodoSchema, *, exclude_unset: bool = False) -> dict:
    """Return a dictionary representation compatible with different Pydantic versions."""

    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_unset=exclude_unset)
    return model.dict(exclude_unset=exclude_unset)


class TodoNotFoundError(Exception):
    """Raised when a todo item cannot be found for a given user."""

    pass


class TodoService:
    """Service layer responsible for managing todo items."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_todos(
        self,
        *,
        user_id: int,
        status: Optional[TodoStatus] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[TodoItem]:
        """Return todo items owned by the given user with optional filters."""

        query = select(TodoItem).where(TodoItem.user_id == user_id)
        if status is not None:
            query = query.where(TodoItem.status == status)
        query = query.order_by(TodoItem.created_at.desc()).offset(skip).limit(limit)
        return self.db.execute(query).scalars().all()

    def get_todo(self, *, todo_id: int, user_id: int) -> TodoItem:
        """Retrieve a single todo item owned by the user."""

        return self._get_owned_todo(todo_id=todo_id, user_id=user_id)

    def create_todo(self, *, user_id: int, todo_in: TodoCreate) -> TodoItem:
        """Create a new todo item for the given user."""

        todo = TodoItem(**_model_to_dict(todo_in), user_id=user_id)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update_todo(
        self, *, todo_id: int, user_id: int, todo_in: TodoUpdate
    ) -> TodoItem:
        """Update an existing todo item while validating ownership."""

        todo = self._get_owned_todo(todo_id=todo_id, user_id=user_id)
        data = _model_to_dict(todo_in, exclude_unset=True)
        for field, value in data.items():
            setattr(todo, field, value)
        todo.updated_at = datetime.utcnow()
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def delete_todo(self, *, todo_id: int, user_id: int) -> None:
        """Delete a todo item owned by the user."""

        todo = self._get_owned_todo(todo_id=todo_id, user_id=user_id)
        self.db.delete(todo)
        self.db.commit()

    def _get_owned_todo(self, *, todo_id: int, user_id: int) -> TodoItem:
        todo = self.db.get(TodoItem, todo_id)
        if todo is None or todo.user_id != user_id:
            raise TodoNotFoundError("Todo item not found.")
        return todo
