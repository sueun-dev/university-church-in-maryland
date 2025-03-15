import os
from .config import Config


def allowed_file(filename: str) -> bool:
    """허용된 확장자인지 확인"""
    if not filename or not isinstance(filename, str):
        return False
    _, ext = os.path.splitext(filename)
    return bool(ext) and ext[1:].lower() in Config.ALLOWED_EXTENSIONS
