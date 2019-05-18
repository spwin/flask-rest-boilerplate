"""create forgot password table

Revision ID: be761be0537a
Revises: 2452fd0e34f9
Create Date: 2019-05-16 21:40:10.351934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be761be0537a'
down_revision = '2452fd0e34f9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'forgot_password',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('hash', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('hash', 'user_id')
    )


def downgrade():
    op.drop_table('forgot_password')
