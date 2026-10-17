"""Make legacy lesson note columns compatible with metadata-only notes

Revision ID: d1e2f3a4b5c6
Revises: c7d8a9e4b1f2
Create Date: 2026-10-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd1e2f3a4b5c6'
down_revision: Union[str, Sequence[str], None] = 'c7d8a9e4b1f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Bring the live lesson_notes table in line with the metadata-only note model."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name'] for col in inspector.get_columns('lesson_notes')}

    if 'duration_seconds' not in columns:
        op.add_column('lesson_notes', sa.Column('duration_seconds', sa.Integer(), nullable=True))

    if 'school_id' in columns:
        op.alter_column('lesson_notes', 'school_id', existing_type=sa.UUID(), nullable=True)
    if 'file_url' in columns:
        op.alter_column('lesson_notes', 'file_url', existing_type=sa.String(length=512), nullable=True)
    if 'original_file_name' in columns:
        op.alter_column('lesson_notes', 'original_file_name', existing_type=sa.String(length=255), nullable=True)


def downgrade() -> None:
    """Restore the pre-refactor legacy NOTE constraints if needed."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col['name'] for col in inspector.get_columns('lesson_notes')}

    if 'original_file_name' in columns:
        op.alter_column('lesson_notes', 'original_file_name', existing_type=sa.String(length=255), nullable=False)
    if 'file_url' in columns:
        op.alter_column('lesson_notes', 'file_url', existing_type=sa.String(length=512), nullable=False)
    if 'school_id' in columns:
        op.alter_column('lesson_notes', 'school_id', existing_type=sa.UUID(), nullable=False)
    if 'duration_seconds' in columns:
        op.drop_column('lesson_notes', 'duration_seconds')
