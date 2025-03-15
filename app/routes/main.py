import os
import time
from datetime import datetime, timedelta
from typing import Any, List, Dict, Tuple
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    send_from_directory,
    Response,
    session,
)
from werkzeug.utils import secure_filename
from flask.views import MethodView

from .. import db
from ..models import PDFFile, Post
from ..config import Config
from ..decorators import check_auth, authenticate, requires_auth
from ..utils import allowed_file

bp = Blueprint("main", __name__)

# Ensure the upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


def mark_new_files(files: List[PDFFile]) -> None:
    """Mark files uploaded within the last 7 days as new."""
    now = datetime.utcnow()
    for file in files:
        setattr(file, "is_new", (now - file.upload_date) <= timedelta(days=7))


def get_files_with_new_flag() -> List[PDFFile]:
    """Retrieve all files from the database and mark new ones."""
    files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    mark_new_files(files)
    return files


def verify_auth() -> bool:
    """
    Helper function to verify request authorization for file-related endpoints.
    Returns True if the credentials are present and valid; otherwise, False.
    """
    auth = request.authorization
    return bool(auth and auth.username and auth.password and check_auth(auth.username, auth.password))


# --- LOGIN ATTEMPT LOCKOUT LOGIC ---

# Constants for login security
LOGIN_MAX_ATTEMPTS = 5
LOGIN_BLOCK_TIME = 30 * 60  # 30 minutes in seconds

# Dictionary to track login attempts per IP address.
login_attempts_login: Dict[str, Tuple[int, float]] = {}


def is_ip_blocked_login(ip: str) -> bool:
    """
    Check if the IP is currently blocked based on the number of failed login attempts.
    """
    if ip in login_attempts_login:
        attempts, last_attempt = login_attempts_login[ip]
        if attempts >= LOGIN_MAX_ATTEMPTS and (time.time() - last_attempt) < LOGIN_BLOCK_TIME:
            return True
    return False


def register_failed_login(ip: str) -> int:
    """
    Record a failed login attempt for the given IP and return the number of remaining attempts.
    """
    if ip in login_attempts_login:
        attempts, _ = login_attempts_login[ip]
        login_attempts_login[ip] = (attempts + 1, time.time())
    else:
        login_attempts_login[ip] = (1, time.time())
    return LOGIN_MAX_ATTEMPTS - login_attempts_login[ip][0]


# --- END OF LOGIN LOCKOUT LOGIC ---


@bp.route("/")
def index() -> str:
    """Render the main page with the regular user chat widget."""
    return render_template("index.html")


@bp.route("/pastor-chat")
@requires_auth()
def pastor_chat() -> str:
    """Render the pastor's chat page (authentication required)."""
    return render_template("pastor_chat.html")


class PostView(MethodView):
    """Handle displaying and posting articles."""

    def get(self) -> str:
        posts = Post.query.order_by(Post.created_at.desc()).all()
        is_pastor = bool(session.get("is_pastor"))
        return render_template("read.html", posts=posts, is_pastor=is_pastor)

    @requires_auth()
    def post(self) -> Any:
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title or not content:
            flash("제목과 내용을 모두 입력해 주세요.", "danger")
            return redirect(url_for("main.read_posts"))
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        flash("게시글이 성공적으로 등록되었습니다.", "success")
        return redirect(url_for("main.read_posts"))


# Register the view with the endpoint name "read_posts"
post_view = PostView.as_view("read_posts")
bp.add_url_rule("/read", view_func=post_view, methods=["GET", "POST"])


@bp.route("/delete_post/<int:post_id>", methods=["POST"])
@requires_auth()
def delete_post(post_id: int) -> Any:
    """Delete a post (admin only)."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("게시글이 삭제되었습니다.", "success")
    return redirect(url_for("main.read_posts"))


@bp.route("/upload", methods=["GET", "POST"])
def upload_file() -> Any:
    """Handle file uploads."""
    if request.method == "POST":
        if not verify_auth():
            return authenticate()
        if "file_input" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files["file_input"]
        original_filename = file.filename or ""
        if not original_filename:
            flash("No selected file", "danger")
            return redirect(request.url)
        if not allowed_file(original_filename):
            flash("File type not allowed", "danger")
            return redirect(request.url)
        safe_filename = secure_filename(original_filename)
        if not safe_filename:
            _, ext = os.path.splitext(original_filename)
            safe_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
        file.save(filepath)
        new_file = PDFFile(filename=original_filename, disk_filename=safe_filename)
        db.session.add(new_file)
        db.session.commit()
        files = get_files_with_new_flag()
        return render_template("upload.html", files=files, success=True)
    files = get_files_with_new_flag()
    return render_template("upload.html", files=files, success=False)


@bp.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id: int) -> Any:
    """Delete a file record and remove the file from disk."""
    if not verify_auth():
        return authenticate()
    file_to_delete = PDFFile.query.get_or_404(file_id)
    filepath = os.path.join(Config.UPLOAD_FOLDER, file_to_delete.disk_filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(file_to_delete)
    db.session.commit()
    flash(f"File {file_to_delete.filename} deleted successfully!", "success")
    return redirect(url_for("main.upload_file"))


@bp.route("/download/<int:file_id>")
def download_file(file_id: int) -> Response:
    """Download a file from the server."""
    file_record = PDFFile.query.get_or_404(file_id)
    return send_from_directory(Config.UPLOAD_FOLDER, file_record.disk_filename)


@bp.route("/robots.txt")
def robots_txt() -> Response:
    """Return a robots.txt file for web crawlers."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://www.uchurchmd.org/sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@bp.route("/api")
def api() -> Response:
    """Provide a JSON API endpoint for retrieving uploaded file info."""
    files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    file_list = [
        {
            "id": f.id,
            "filename": f.filename,
            "upload_date": f.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for f in files
    ]
    return jsonify(file_list)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Any:
    """
    Handle user login with a 30-minute lockout for excessive failed attempts.
    Only valid credentials (i.e. pastors) are accepted.
    """
    ip = request.remote_addr
    if request.method == "POST":
        # Check if the IP is currently blocked
        if is_ip_blocked_login(ip):
            flash("로그인 시도가 너무 많습니다. 30분 후에 다시 시도해 주세요.", "danger")
            return render_template("login.html")
        
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if check_auth(username, password):
            # Successful login: clear any recorded failed attempts for this IP
            if ip in login_attempts_login:
                del login_attempts_login[ip]
            session["is_pastor"] = True
            flash("로그인에 성공했습니다.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.read_posts"))
        else:
            remaining_attempts = register_failed_login(ip)
            if remaining_attempts <= 0:
                flash("로그인 시도가 너무 많습니다. 30분 후에 다시 시도해 주세요.", "danger")
            else:
                flash(f"로그인 정보가 올바르지 않습니다. 남은 시도: {remaining_attempts}", "danger")
    return render_template("login.html")


@bp.route("/logout")
def logout() -> Any:
    """Log out the current user."""
    session.pop("is_pastor", None)
    flash("로그아웃되었습니다.", "success")
    return redirect(url_for("main.index"))
