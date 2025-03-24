from . import db
from datetime import datetime

class PDFFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    disk_filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    def __init__(self, *, filename: str, disk_filename: str) -> None:
        self.filename = filename
        self.disk_filename = disk_filename

    def __repr__(self) -> str:
        return f"PDFFile('{self.filename}', '{self.upload_date}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='general')  # ✅ Added category field
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    def __init__(self, *, title: str, content: str, category: str = 'general') -> None:
        self.title = title
        self.content = content
        self.category = category  # ✅ Updated constructor

    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.category}', '{self.created_at}')"

class ZoomLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
