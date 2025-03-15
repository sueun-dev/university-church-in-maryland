import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()


class Config:
    """Flask 애플리케이션 설정"""

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # 파일 업로드 설정
    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "uploads"
    )
    MAX_CONTENT_LENGTH = 24 * 1024 * 1024  # 24 MB
    ALLOWED_EXTENSIONS = {
        "pdf",
        "docx",
        "png",
        "jpeg",
        "jpg",
        "gif",
        "bmp",
        "svg",
        "txt",
        "rtf",
        "csv",
        "html",
    }

    # 인증 설정 (업로드, pastor 채팅)
    USERNAME = os.getenv("UPLOAD_USERNAME", "admin")
    UPLOAD_PASSWORD_HASH = generate_password_hash(
        os.getenv("UPLOAD_PASSWORD", "password"), method="pbkdf2:sha256"
    )

    # 로그인 시도 제한
    MAX_ATTEMPTS = 7
    BLOCK_TIME = 24 * 60 * 60  # 24시간
