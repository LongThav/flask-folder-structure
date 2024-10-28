"""add role model

Revision ID: 7b660f5d2b14
Revises: 9115fd164584
Create Date: 2024-05-31 23:03:28.374181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b660f5d2b14'
down_revision = '9115fd164584'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tbl_role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('tbl_role')
