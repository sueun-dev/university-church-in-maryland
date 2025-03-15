import time
from functools import wraps
from typing import Callable, Any, Dict, Tuple
from flask import request, session, redirect, url_for
from werkzeug.security import check_password_hash
from .config import Config

# 로그인 시도 추적 (데모용)
login_attempts: Dict[str, Tuple[int, float]] = {}


def check_auth(username: str, password: str) -> bool:
    """자격 증명 확인"""
    return username == Config.USERNAME and check_password_hash(
        Config.UPLOAD_PASSWORD_HASH, password
    )


def authenticate():
    """인증되지 않은 요청은 로그인 페이지로 리디렉션"""
    return redirect(url_for("main.login", next=request.url))


def is_ip_blocked(ip: str) -> bool:
    """IP 차단 여부 확인"""
    if ip in login_attempts:
        attempts, last_attempt = login_attempts[ip]
        if (
            attempts >= Config.MAX_ATTEMPTS
            and (time.time() - last_attempt) < Config.BLOCK_TIME
        ):
            return True
    return False


def register_failed_attempt(ip: str) -> int:
    """실패한 로그인 시도 기록"""
    if ip in login_attempts:
        attempts, _ = login_attempts[ip]
        login_attempts[ip] = (attempts + 1, time.time())
    else:
        login_attempts[ip] = (1, time.time())
    remaining_attempts = Config.MAX_ATTEMPTS - login_attempts[ip][0]
    return remaining_attempts


def requires_auth(force_reauth: bool = False) -> Callable:
    """인증 필요 데코레이터"""

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            if session.get("is_pastor"):
                return f(*args, **kwargs)
            return redirect(url_for("main.login", next=request.url))

        return wrapped

    return decorator
