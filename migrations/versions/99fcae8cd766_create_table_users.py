"""create table users

Revision ID: 99fcae8cd766
Revises: eda3791bb029
Create Date: 2019-05-16 08:31:48.716734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99fcae8cd766'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('public_id', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('first_name', sa.String(length=200), nullable=True),
        sa.Column('last_name', sa.String(length=200), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=100), nullable=True),
        sa.Column('admin', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('status', sa.Integer(), nullable=False, server_default=sa.schema.DefaultClause("0")),
        sa.Column('verified', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('deleted_at', sa.Boolean(), nullable=True),
        sa.Column('registered_on', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('public_id'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('users')
