"""Merge the note compatibility migration heads.

Revision ID: e4f5a6b7c8d9
Revises: 9c4e7f1a2b3c, d1e2f3a4b5c6
Create Date: 2026-10-17 08:35:00.000000

Both parent migrations make the legacy lesson note columns nullable. This
revision only joins the existing branches so Alembic has a single head.
"""

from typing import Sequence, Union


revision: str = "e4f5a6b7c8d9"
down_revision: Union[str, Sequence[str], None] = (
    "9c4e7f1a2b3c",
    "d1e2f3a4b5c6",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge migration branches without changing the database."""
    pass


def downgrade() -> None:
    """Separate the migration branches again."""
    pass
