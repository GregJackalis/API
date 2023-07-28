"""add user table

Revision ID: b517d920c3e4
Revises: ea025acb24d6
Create Date: 2023-07-28 15:58:20.867950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b517d920c3e4'
down_revision = 'ea025acb24d6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("Users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_At", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("Users")
    pass
