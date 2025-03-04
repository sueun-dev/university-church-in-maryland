# models.py
from . import db


class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Store the original filename (Korean allowed)
    filename = db.Column(db.String(255), nullable=False)

    # Store the sanitized filename for saving on disk
    disk_filename = db.Column(db.String(255), nullable=False)

    upload_date = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    def __init__(self, filename, disk_filename):
        self.filename = filename
        self.disk_filename = disk_filename

    def __repr__(self):
        return f"PDFFile('{self.filename}', '{self.upload_date}')"
