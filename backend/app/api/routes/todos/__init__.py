"""API router providing CRUD endpoints for todo items."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.dependencies.auth import get_current_user
from backend.app.models.todo import TodoStatus
from backend.app.models.user import User
from backend.app.schemas.todo import TodoCreate, TodoRead, TodoUpdate
from backend.app.services.todo_service import TodoNotFoundError, TodoService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[TodoRead])
def list_todos(
    *,
    status: Optional[TodoStatus] = Query(None, description="Filter by todo status."),
    skip: int = Query(0, ge=0, description="Number of items to skip."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of items to return."),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TodoRead]:
    """Return a paginated list of todos for the current user."""

    service = TodoService(db)
    todos = service.list_todos(
        user_id=current_user.id, status=status, skip=skip, limit=limit
    )
    return todos


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    *,
    todo_in: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoRead:
    """Create a new todo item for the current user."""

    service = TodoService(db)
    todo = service.create_todo(user_id=current_user.id, todo_in=todo_in)
    return todo


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    *,
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoRead:
    """Retrieve a single todo item owned by the current user."""

    service = TodoService(db)
    try:
        return service.get_todo(todo_id=todo_id, user_id=current_user.id)
    except TodoNotFoundError as exc:  # pragma: no cover - simple passthrough
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    *,
    todo_id: int,
    todo_in: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TodoRead:
    """Update a todo item belonging to the current user."""

    service = TodoService(db)
    try:
        return service.update_todo(
            todo_id=todo_id, user_id=current_user.id, todo_in=todo_in
        )
    except TodoNotFoundError as exc:  # pragma: no cover - simple passthrough
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    *,
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a todo item belonging to the current user."""

    service = TodoService(db)
    try:
        service.delete_todo(todo_id=todo_id, user_id=current_user.id)
    except TodoNotFoundError as exc:  # pragma: no cover - simple passthrough
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
