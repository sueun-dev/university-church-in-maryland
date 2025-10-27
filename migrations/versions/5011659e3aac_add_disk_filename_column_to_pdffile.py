"""Add disk_filename column to PDFFile

Revision ID: 5011659e3aac
Revises: 524b262ce399
Create Date: 2025-03-04 17:32:37.358962

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5011659e3aac"
down_revision = "524b262ce399"
branch_labels = None
depends_on = None


def _refresh_metadata(bind):
    inspector = sa.inspect(bind)
    return inspector, set(inspector.get_table_names())


def upgrade():
    bind = op.get_bind()
    inspector, tables = _refresh_metadata(bind)

    if "pdf_files" in tables:
        op.drop_table("pdf_files")
        inspector, tables = _refresh_metadata(bind)

    if "pdf_file" not in tables:
        op.create_table(
            "pdf_file",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("filename", sa.String(length=255), nullable=False),
            sa.Column("disk_filename", sa.String(length=255), nullable=False),
            sa.Column("upload_date", sa.DateTime(), nullable=False),
        )
        return

    columns = {col["name"] for col in inspector.get_columns("pdf_file")}
    with op.batch_alter_table("pdf_file", schema=None) as batch_op:
        if "disk_filename" not in columns:
            batch_op.add_column(
                sa.Column("disk_filename", sa.String(length=255), nullable=False)
            )
        batch_op.alter_column(
            "filename",
            existing_type=sa.VARCHAR(length=120),
            type_=sa.String(length=255),
            existing_nullable=False,
        )


def downgrade():
    bind = op.get_bind()
    inspector, tables = _refresh_metadata(bind)

    if "pdf_file" in tables:
        columns = {col["name"] for col in inspector.get_columns("pdf_file")}
        with op.batch_alter_table("pdf_file", schema=None) as batch_op:
            if "disk_filename" in columns:
                batch_op.drop_column("disk_filename")
            batch_op.alter_column(
                "filename",
                existing_type=sa.String(length=255),
                type_=sa.VARCHAR(length=120),
                existing_nullable=False,
            )

    inspector, tables = _refresh_metadata(bind)
    if "pdf_files" not in tables:
        op.create_table(
            "pdf_files",
            sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
            sa.Column(
                "filename", sa.VARCHAR(length=120), autoincrement=False, nullable=False
            ),
            sa.Column(
                "upload_date",
                postgresql.TIMESTAMP(),
                autoincrement=False,
                nullable=False,
            ),
            sa.PrimaryKeyConstraint("id", name="pdf_files_pkey"),
        )
