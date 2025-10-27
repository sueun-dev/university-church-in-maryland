"""Add category to Post

Revision ID: 808e30267346
Revises: 5011659e3aac
Create Date: 2025-03-24 02:04:04.559176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '808e30267346'
down_revision = '5011659e3aac'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "post" not in existing_tables:
        op.create_table(
            'post',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('category', sa.String(length=50), nullable=False, server_default='general'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        )
        return

    columns = {col["name"] for col in inspector.get_columns("post")}

    if "category" in columns:
        return

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=False, server_default='general'))

    op.execute("UPDATE post SET category='general' WHERE category IS NULL")
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('category', server_default=None)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "post" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("post")}
    if "category" not in columns:
        return

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('category')
