"""add content column to Posts table

Revision ID: ea025acb24d6
Revises: 1808cee49527
Create Date: 2023-07-28 15:37:12.894599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea025acb24d6'
down_revision = '1808cee49527'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Posts", sa.Column("Content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("Posts", "Content")
    pass
