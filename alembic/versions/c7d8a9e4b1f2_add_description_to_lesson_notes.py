"""Add description column to lesson_notes

Revision ID: c7d8a9e4b1f2
Revises: b2e7c4a19f30
Create Date: 2026-10-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7d8a9e4b1f2'
down_revision: Union[str, Sequence[str], None] = 'b2e7c4a19f30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Align legacy lesson_note table with the note model and metadata upload flow."""
    # Some deployments still carry the older non-null school/file constraints
    # from the pre-class refactor. Metadata uploads are valid without these
    # values, so the DB needs to match the app contract.
    op.add_column('lesson_notes', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('lesson_notes', sa.Column('duration_seconds', sa.Integer(), nullable=True))

    op.alter_column('lesson_notes', 'school_id', existing_type=sa.UUID(), nullable=True)
    op.alter_column('lesson_notes', 'file_url', existing_type=sa.String(length=512), nullable=True)
    op.alter_column('lesson_notes', 'original_file_name', existing_type=sa.String(length=255), nullable=True)


def downgrade() -> None:
    """Undo the compatibility changes for the lesson note table."""
    op.alter_column('lesson_notes', 'original_file_name', existing_type=sa.String(length=255), nullable=False)
    op.alter_column('lesson_notes', 'file_url', existing_type=sa.String(length=512), nullable=False)
    op.alter_column('lesson_notes', 'school_id', existing_type=sa.UUID(), nullable=False)
    op.drop_column('lesson_notes', 'duration_seconds')
    op.drop_column('lesson_notes', 'description')
