import os
from .config import Config


def allowed_file(filename: str) -> bool:
    """
    Check if the given filename has an allowed extension.

    The function uses os.path.splitext to reliably extract the extension,
    converts it to lowercase (excluding the leading period), and checks if
    the extension is listed in the configuration's allowed extensions.

    Args:
        filename (str): The filename to validate.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    if not filename or not isinstance(filename, str):
        return False

    # Extract the file extension
    _, ext = os.path.splitext(filename)
    return bool(ext) and ext[1:].lower() in Config.ALLOWED_EXTENSIONS
