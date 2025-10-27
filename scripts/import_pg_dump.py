"""Import selected tables from a PostgreSQL dump (COPY format) into SQLite.

The production DB is PostgreSQL, but local development uses SQLite. This script
parses the COPY sections for a few known tables (pdf_file, post, site_content,
zoom_link) and inserts the rows via SQLAlchemy models.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path
import re
from typing import Dict, List, Tuple

from app import create_app, db
from app.models import PDFFile, Post, SiteContent, ZoomLink


TABLE_MODELS = {
    "pdf_file": PDFFile,
    "post": Post,
    "site_content": SiteContent,
    "zoom_link": ZoomLink,
}

COPY_PATTERN = re.compile(r"^COPY public\.(\w+) \(([^)]+)\) FROM stdin;$")


def _parse_copy_blocks(dump_path: Path) -> Dict[str, Tuple[List[str], List[List[str]]]]:
    blocks: Dict[str, Tuple[List[str], List[List[str]]]] = {}
    with dump_path.open("r", encoding="utf-8") as dump_fd:
        lines = dump_fd.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip("\n")
        match = COPY_PATTERN.match(line)
        if not match:
            i += 1
            continue

        table_name = match.group(1)
        columns = [
            column.strip().strip('"')
            for column in match.group(2).split(",")
        ]

        i += 1
        data_rows: List[List[str]] = []
        dialect = csv.excel_tab
        dialect.quoting = csv.QUOTE_NONE  # COPY output is raw, no quoting
        while i < len(lines):
            raw_row = lines[i].rstrip("\n")
            if raw_row == r"\.":
                break
            reader = csv.reader([raw_row], dialect=dialect)
            values = next(reader)
            data_rows.append(values)
            i += 1

        blocks[table_name] = (columns, data_rows)
        i += 1  # Skip the terminating '\.'

    return blocks


def _convert_value(value: str) -> str | None:
    if value == r"\N":
        return None
    return value.replace(r"\r\n", "\n")


def _parse_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    if "." in value:
        prefix, fraction = value.split(".", 1)
        fraction = fraction.rstrip("Z")
        if len(fraction) > 6:
            fraction = fraction[:6]
        else:
            fraction = fraction.ljust(6, "0")
        value = f"{prefix}.{fraction}"
    return dt.datetime.fromisoformat(value)


def import_dump(dump_path: Path) -> None:
    copy_blocks = _parse_copy_blocks(dump_path)
    app = create_app()
    with app.app_context():
        # Clear tables to avoid duplication.
        db.session.execute(db.text("DELETE FROM pdf_file"))
        db.session.execute(db.text("DELETE FROM post"))
        db.session.execute(db.text("DELETE FROM site_content"))
        db.session.execute(db.text("DELETE FROM zoom_link"))

        for table_name, (columns, rows) in copy_blocks.items():
            if table_name not in TABLE_MODELS:
                continue
            Model = TABLE_MODELS[table_name]
            for row in rows:
                data = {
                    column: _convert_value(value)
                    for column, value in zip(columns, row)
                }
                if "id" in data and data["id"] is not None:
                    data["id"] = int(data["id"])
                if table_name == "pdf_file":
                    if data.get("upload_date"):
                        data["upload_date"] = _parse_datetime(data["upload_date"])
                    instance = Model(
                        filename=data["filename"],
                        disk_filename=data["disk_filename"],
                    )
                    instance.id = data["id"]
                    instance.upload_date = data["upload_date"]
                elif table_name == "post":
                    if data.get("created_at"):
                        data["created_at"] = _parse_datetime(data["created_at"])
                    instance = Model(
                        title=data["title"],
                        content=data["content"],
                        category=data["category"],
                    )
                    instance.id = data["id"]
                    instance.created_at = data["created_at"]
                elif table_name == "site_content":
                    if data.get("updated_at"):
                        data["updated_at"] = _parse_datetime(data["updated_at"])
                    instance = Model(
                        key=data["key"],
                        title=data["title"],
                        content=data["content"],
                    )
                    instance.id = data["id"]
                    instance.updated_at = data.get("updated_at")
                elif table_name == "zoom_link":
                    if data.get("updated_at"):
                        data["updated_at"] = _parse_datetime(data["updated_at"])
                    instance = Model(
                        url=data["url"],
                    )
                    instance.id = data["id"]
                    instance.password = data.get("password")
                    instance.updated_at = data.get("updated_at")
                else:
                    continue

                db.session.merge(instance)

        db.session.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Import selected tables from a PostgreSQL dump.")
    parser.add_argument("dump_path", type=Path, help="Path to the .sql dump created by pg_dump")
    args = parser.parse_args()

    import_dump(args.dump_path)


if __name__ == "__main__":
    main()
