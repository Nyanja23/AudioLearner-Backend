"""Add class-based tables.

Revision ID: 7d2f6c8a4b91
Revises: 18610ce9ee70
Create Date: 2026-10-13 09:54:24.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d2f6c8a4b91"
down_revision: Union[str, Sequence[str], None] = "18610ce9ee70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the class hierarchy used by lesson notes."""
    op.create_table(
        "classes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("class_name", sa.String(length=255), nullable=False),
        sa.Column("class_teacher_id", sa.UUID(), nullable=False),
        sa.Column("student_code", sa.String(length=10), nullable=False),
        sa.Column("teacher_code", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["class_teacher_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_code"),
        sa.UniqueConstraint("teacher_code"),
    )
    op.create_index(
        op.f("ix_classes_class_teacher_id"),
        "classes",
        ["class_teacher_id"],
        unique=False,
    )
    op.create_index("idx_class_teacher", "classes", ["class_teacher_id"], unique=False)

    op.create_table(
        "class_subjects",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("class_id", sa.UUID(), nullable=False),
        sa.Column("subject_name", sa.String(length=100), nullable=False),
        sa.Column("subject_teacher_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
        sa.ForeignKeyConstraint(["subject_teacher_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_class_subjects_class_id"),
        "class_subjects",
        ["class_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_class_subjects_subject_teacher_id"),
        "class_subjects",
        ["subject_teacher_id"],
        unique=False,
    )
    op.create_index("idx_class_subject_class", "class_subjects", ["class_id"], unique=False)
    op.create_index(
        "idx_class_subject_teacher",
        "class_subjects",
        ["subject_teacher_id"],
        unique=False,
    )

    op.create_table(
        "class_memberships",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("class_id", sa.UUID(), nullable=False),
        sa.Column("student_id", sa.UUID(), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("left_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_class_memberships_class_id"),
        "class_memberships",
        ["class_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_class_memberships_student_id"),
        "class_memberships",
        ["student_id"],
        unique=False,
    )
    op.create_index(
        "idx_class_membership_class_student",
        "class_memberships",
        ["class_id", "student_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the class hierarchy tables."""
    op.drop_index("idx_class_membership_class_student", table_name="class_memberships")
    op.drop_index(op.f("ix_class_memberships_student_id"), table_name="class_memberships")
    op.drop_index(op.f("ix_class_memberships_class_id"), table_name="class_memberships")
    op.drop_table("class_memberships")

    op.drop_index("idx_class_subject_teacher", table_name="class_subjects")
    op.drop_index("idx_class_subject_class", table_name="class_subjects")
    op.drop_index(op.f("ix_class_subjects_subject_teacher_id"), table_name="class_subjects")
    op.drop_index(op.f("ix_class_subjects_class_id"), table_name="class_subjects")
    op.drop_table("class_subjects")

    op.drop_index("idx_class_teacher", table_name="classes")
    op.drop_index(op.f("ix_classes_class_teacher_id"), table_name="classes")
    op.drop_table("classes")
