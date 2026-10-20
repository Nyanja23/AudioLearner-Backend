"""Make legacy lesson note fields nullable.

Revision ID: 9c4e7f1a2b3c
Revises: b2e7c4a19f30
Create Date: 2026-10-17 08:30:00.000000

The class-based note model no longer writes the legacy school_id, file_url,
or original_file_name fields. They were still non-nullable in the initial
migration, causing metadata-only uploads to fail during INSERT.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c4e7f1a2b3c"
down_revision: Union[str, Sequence[str], None] = "b2e7c4a19f30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Allow note records to omit fields no longer used by the model."""
    op.alter_column(
        "lesson_notes",
        "school_id",
        existing_type=sa.UUID(),
        nullable=True,
    )
    op.alter_column(
        "lesson_notes",
        "file_url",
        existing_type=sa.String(length=512),
        nullable=True,
    )
    op.alter_column(
        "lesson_notes",
        "original_file_name",
        existing_type=sa.String(length=255),
        nullable=True,
    )


def downgrade() -> None:
    """Restore the original constraints for legacy deployments."""
    op.alter_column(
        "lesson_notes",
        "school_id",
        existing_type=sa.UUID(),
        nullable=False,
    )
    op.alter_column(
        "lesson_notes",
        "file_url",
        existing_type=sa.String(length=512),
        nullable=False,
    )
    op.alter_column(
        "lesson_notes",
        "original_file_name",
        existing_type=sa.String(length=255),
        nullable=False,
    )
