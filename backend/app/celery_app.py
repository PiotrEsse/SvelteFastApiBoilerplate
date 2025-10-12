"""Celery application instance and beat schedule configuration."""

from __future__ import annotations

import os
from datetime import timedelta

from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", BROKER_URL)
TIMEZONE = os.getenv("CELERY_TIMEZONE", "UTC")
REMINDER_INTERVAL_MINUTES = int(os.getenv("REMINDER_INTERVAL_MINUTES", "60"))

celery_app = Celery(
    "backend.app",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["backend.app.tasks.reminders"],
)

celery_app.conf.timezone = TIMEZONE
celery_app.conf.beat_schedule = {
    "send-due-notifications": {
        "task": "backend.app.tasks.reminders.send_due_notifications",
        "schedule": timedelta(minutes=REMINDER_INTERVAL_MINUTES),
    }
}

celery_app.autodiscover_tasks(lambda: ["backend.app.tasks"])
