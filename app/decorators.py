import time
from functools import wraps
from typing import Callable, Any, Dict, Tuple
from flask import request, Response
from werkzeug.security import check_password_hash
from .config import Config
from .exceptions import InvalidUsage

# In-memory login attempt tracker (for demonstration purposes)
login_attempts: Dict[str, Tuple[int, float]] = {}


def check_auth(username: str, password: str) -> bool:
    """
    Validate credentials against the configuration.
    """
    return username == Config.USERNAME and check_password_hash(
        Config.UPLOAD_PASSWORD_HASH, password
    )


def authenticate() -> Response:
    """
    Generate a 401 response that prompts for authentication.
    """
    html_response = """
    <html>
        <body>
            <h2>Authentication Required</h2>
            <p>Please enter the correct username and password.</p>
            <button onclick="window.location.href='/'">Go to Home</button>
        </body>
    </html>
    """
    return Response(
        html_response,
        status=401,
        headers={"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def is_ip_blocked(ip: str) -> bool:
    """
    Check if an IP address is blocked based on failed login attempts.
    """
    if ip in login_attempts:
        attempts, last_attempt = login_attempts[ip]
        if (
            attempts >= Config.MAX_ATTEMPTS
            and (time.time() - last_attempt) < Config.BLOCK_TIME
        ):
            return True
    return False


def register_failed_attempt(ip: str) -> int:
    """
    Record a failed login attempt for a given IP address and return the remaining attempts.
    """
    if ip in login_attempts:
        attempts, _ = login_attempts[ip]
        login_attempts[ip] = (attempts + 1, time.time())
    else:
        login_attempts[ip] = (1, time.time())
    remaining_attempts = Config.MAX_ATTEMPTS - login_attempts[ip][0]
    return remaining_attempts


def requires_auth(force_reauth: bool = False) -> Callable:
    """
    Decorator to enforce basic authentication on a Flask view.
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            ip: str = request.remote_addr  # type: ignore
            if is_ip_blocked(ip):
                raise InvalidUsage(
                    "Your IP is blocked due to too many failed login attempts.",
                    status_code=403,
                )
            auth = request.authorization
            if (
                not auth
                or auth.username is None
                or auth.password is None
                or not check_auth(auth.username, auth.password)
                or force_reauth
            ):
                register_failed_attempt(ip)
                return authenticate()
            return f(*args, **kwargs)

        return decorated

    return decorator


__all__ = [
    "check_auth",
    "authenticate",
    "is_ip_blocked",
    "register_failed_attempt",
    "requires_auth",
    "login_attempts",
]
