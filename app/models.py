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
    category = db.Column(db.String(50), nullable=False, default='general')
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    def __init__(self, *, title: str, content: str, category: str = 'general') -> None:
        self.title = title
        self.content = content
        self.category = category

    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.category}', '{self.created_at}')"

class ZoomLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(50), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SiteContent(db.Model):
    """사이트 콘텐츠 저장을 위한 모델"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)  # 콘텐츠 식별자 (welcome_message, about_church 등)
    title = db.Column(db.String(100), nullable=False)  # 콘텐츠 제목
    content = db.Column(db.Text, nullable=False)  # 콘텐츠 내용
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Message(db.Model):
    """교인들이 목사님에게 남기는 메시지 모델"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 작성자 이름
    email = db.Column(db.String(100), nullable=True)  # 답변받을 이메일 (선택)
    subject = db.Column(db.String(200), nullable=False)  # 메시지 제목
    content = db.Column(db.Text, nullable=False)  # 메시지 내용
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 작성 시간
    is_read = db.Column(db.Boolean, default=False)  # 읽음 상태
