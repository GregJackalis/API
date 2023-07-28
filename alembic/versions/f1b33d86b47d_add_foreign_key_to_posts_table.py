"""add foreign key to Posts table

Revision ID: f1b33d86b47d
Revises: b517d920c3e4
Create Date: 2023-07-28 16:13:41.742774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1b33d86b47d'
down_revision = 'b517d920c3e4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="Posts", referent_table="Users",
                          local_cols=["owner_id"], 
                          remote_cols=["id"], 
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="Posts")
    op.drop_column("Posts", "owner_id")
    pass
