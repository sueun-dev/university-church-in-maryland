"""Add ZoomLink model

Revision ID: e9cfe31316e4
Revises: 808e30267346
Create Date: 2025-03-24 02:33:06.512360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9cfe31316e4'
down_revision = '808e30267346'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'zoom_link' in inspector.get_table_names():
        return

    op.create_table(
        'zoom_link',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=255), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'zoom_link' not in inspector.get_table_names():
        return
    op.drop_table('zoom_link')
