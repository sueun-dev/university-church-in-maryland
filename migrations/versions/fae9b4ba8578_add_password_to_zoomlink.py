"""Add password to ZoomLink

Revision ID: fae9b4ba8578
Revises: add_message_table
Create Date: 2025-10-27 00:40:31.132394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fae9b4ba8578'
down_revision = 'add_message_table'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if 'site_content' not in tables:
        op.create_table(
            'site_content',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('key', sa.String(length=50), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('key')
        )

    if 'zoom_link' not in tables:
        op.create_table(
            'zoom_link',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('url', sa.String(length=255), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        tables.add('zoom_link')
        inspector = sa.inspect(bind)

    columns = {col['name'] for col in inspector.get_columns('zoom_link')}
    if 'password' not in columns:
        with op.batch_alter_table('zoom_link', schema=None) as batch_op:
            batch_op.add_column(sa.Column('password', sa.String(length=50), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'zoom_link' in inspector.get_table_names():
        columns = {col['name'] for col in inspector.get_columns('zoom_link')}
        if 'password' in columns:
            with op.batch_alter_table('zoom_link', schema=None) as batch_op:
                batch_op.drop_column('password')

    inspector = sa.inspect(bind)
    if 'site_content' in inspector.get_table_names():
        op.drop_table('site_content')
