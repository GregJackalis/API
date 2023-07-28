"""add last few columns to Posts table

Revision ID: 529d05f73812
Revises: f1b33d86b47d
Create Date: 2023-07-28 16:19:20.796234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '529d05f73812'
down_revision = 'f1b33d86b47d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('Posts', sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    
    op.add_column('Posts', sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts', "published")
    op.drop_column('Posts', "created_at")
    pass