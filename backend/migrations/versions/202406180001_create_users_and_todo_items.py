"""Create users and todo_items tables.

Revision ID: 202406180001
Revises: 
Create Date: 2024-06-18 00:01:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "202406180001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    todo_status_enum = sa.Enum("pending", "in_progress", "completed", name="todo_status")
    todo_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.sql.expression.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index(op.f("ix_users_created_at"), "users", ["created_at"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "todo_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            todo_status_enum,
            nullable=False,
            server_default=sa.text("'pending'"),
        ),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index(op.f("ix_todo_items_created_at"), "todo_items", ["created_at"], unique=False)
    op.create_index(op.f("ix_todo_items_status"), "todo_items", ["status"], unique=False)
    op.create_index(op.f("ix_todo_items_updated_at"), "todo_items", ["updated_at"], unique=False)
    op.create_index(op.f("ix_todo_items_user_id"), "todo_items", ["user_id"], unique=False)
    op.create_index(
        "ix_todo_items_user_status",
        "todo_items",
        ["user_id", "status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_todo_items_user_status", table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_user_id"), table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_updated_at"), table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_status"), table_name="todo_items")
    op.drop_index(op.f("ix_todo_items_created_at"), table_name="todo_items")
    op.drop_table("todo_items")

    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_table("users")

    todo_status_enum = sa.Enum("pending", "in_progress", "completed", name="todo_status")
    todo_status_enum.drop(op.get_bind(), checkfirst=True)
