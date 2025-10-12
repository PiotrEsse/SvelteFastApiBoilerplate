"""Celery tasks responsible for sending reminder notifications."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import select

from backend.app.db.session import session_scope
from backend.app.models.todo import TodoItem, TodoStatus

logger = logging.getLogger(__name__)


@shared_task(name="backend.app.tasks.reminders.send_due_notifications")
def send_due_notifications() -> int:
    """Send notifications for todos due within the next 24 hours.

    Returns the number of notifications that were triggered to aid visibility
    in logs and monitoring. In a real system this function would integrate with
    an email/SMS service – here we log a message for each todo as a placeholder.
    """

    now = datetime.utcnow()
    upcoming = now + timedelta(hours=24)

    with session_scope() as session:
        stmt = (
            select(TodoItem)
            .where(TodoItem.due_date != None)  # noqa: E711 - intentional SQLAlchemy comparison
            .where(TodoItem.status != TodoStatus.COMPLETED)
            .where(TodoItem.due_date <= upcoming)
            .where(TodoItem.due_date >= now)
            .order_by(TodoItem.due_date.asc())
        )
        todos = session.execute(stmt).scalars().all()

    for todo in todos:
        logger.info(
            "[Reminder] Todo %s for user %s is due at %s. Triggering notification...",
            todo.title,
            todo.user_id,
            todo.due_date,
        )

    logger.info("send_due_notifications processed %d todos", len(todos))
    return len(todos)
