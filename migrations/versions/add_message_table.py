"""add message table

Revision ID: add_message_table
Revises: e9cfe31316e4
Create Date: 2025-05-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_message_table'
down_revision = 'e9cfe31316e4'
branch_labels = None
depends_on = None


def upgrade():
    # Create only the message table
    op.create_table('message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Only drop the message table if needed
    op.drop_table('message')
