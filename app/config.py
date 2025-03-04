import os
from typing import Set
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables from the .env file
load_dotenv()


class Config:
    """
    Application configuration settings.

    Attributes:
        SECRET_KEY (str): Secret key for Flask sessions.
        SQLALCHEMY_DATABASE_URI (str): Database URI for SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable modification tracking for performance.
        SQLALCHEMY_ECHO (bool): Enable SQL statement logging (disabled by default).
        UPLOAD_FOLDER (str): Absolute path to the folder for file uploads.
        MAX_CONTENT_LENGTH (int): Maximum allowed size of uploaded content (in bytes).
        ALLOWED_EXTENSIONS (Set[str]): Set of permitted file extensions for uploads.
        USERNAME (str): Username required for upload authentication.
        UPLOAD_PASSWORD_HASH (str): Hashed password for secure upload authentication.
        MAX_ATTEMPTS (int): Maximum number of allowed login attempts before blocking.
        BLOCK_TIME (int): Duration in seconds to block an IP after max failed attempts.
    """

    # Flask configuration
    SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Upload settings
    UPLOAD_FOLDER: str = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "uploads"
    )
    MAX_CONTENT_LENGTH: int = 12 * 1024 * 1024  # 12 MB
    ALLOWED_EXTENSIONS: Set[str] = {
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

    # Authentication settings
    USERNAME: str = os.getenv("UPLOAD_USERNAME", "admin")
    UPLOAD_PASSWORD_HASH: str = generate_password_hash(
        os.getenv("UPLOAD_PASSWORD", "password"), method="pbkdf2:sha256"
    )

    # Login attempt settings
    MAX_ATTEMPTS: int = 7
    BLOCK_TIME: int = 24 * 60 * 60  # 24 hours in seconds


__all__ = ["Config"]
