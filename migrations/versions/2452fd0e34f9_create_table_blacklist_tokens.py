"""create table blacklist_tokens

Revision ID: 2452fd0e34f9
Revises: 99fcae8cd766
Create Date: 2019-05-16 08:34:01.991055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2452fd0e34f9'
down_revision = '99fcae8cd766'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blacklist_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False),
        sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )


def downgrade():
    op.drop_table('blacklist_tokens')
