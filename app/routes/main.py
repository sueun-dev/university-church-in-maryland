import os
from datetime import datetime, timedelta
from typing import Any, List

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
)
from werkzeug.utils import secure_filename

from .. import db
from ..models import PDFFile
from ..config import Config
from ..decorators import check_auth, authenticate
from ..utils import allowed_file

bp = Blueprint("main", __name__)

# Ensure the upload folder exists
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)


def mark_new_files(files: List[PDFFile]) -> None:
    """
    Mark each PDFFile instance with an 'is_new' attribute if it was uploaded within the last 7 days.
    """
    now = datetime.utcnow()
    for file in files:
        # Use setattr to avoid attribute errors during static type checking.
        setattr(file, "is_new", (now - file.upload_date) <= timedelta(days=7))


def get_files_with_new_flag() -> List[PDFFile]:
    """
    Retrieve all PDFFile records ordered by upload_date in descending order and mark them as new if applicable.
    """
    files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    mark_new_files(files)
    return files


@bp.route("/")
def index() -> str:
    """
    Render the index page.
    """
    return render_template("index.html")


@bp.route("/upload", methods=["GET", "POST"])
def upload_file() -> Any:
    """
    Handle file uploads. Validates authentication, file presence, and allowed file extensions.
    Saves the file with a sanitized disk filename and stores both the original and disk filenames in the database.
    """
    if request.method == "POST":
        auth = request.authorization
        if (
            not auth
            or auth.username is None
            or auth.password is None
            or not check_auth(auth.username, auth.password)
        ):
            return authenticate()

        if "file_input" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)

        file = request.files["file_input"]
        raw_filename = file.filename or ""
        if not raw_filename:
            flash("No selected file", "danger")
            return redirect(request.url)

        if not allowed_file(raw_filename):
            flash("File type not allowed", "danger")
            return redirect(request.url)

        # Generate a sanitized filename for disk storage
        disk_name = secure_filename(raw_filename)
        if not disk_name:
            # Fallback: use a timestamp plus the original file extension
            _, ext = os.path.splitext(raw_filename)
            disk_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{ext}"

        filepath = os.path.join(Config.UPLOAD_FOLDER, disk_name)
        file.save(filepath)

        # Create a new record storing both the original (display) and sanitized (disk) filenames
        new_file = PDFFile(filename=raw_filename, disk_filename=disk_name)
        db.session.add(new_file)
        db.session.commit()

        files = get_files_with_new_flag()
        return render_template("upload.html", files=files, success=True)

    files = get_files_with_new_flag()
    return render_template("upload.html", files=files, success=False)


@bp.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id: int) -> Any:
    """
    Delete a file from both the filesystem and the database based on its ID.
    Requires valid authentication.
    """
    auth = request.authorization
    if (
        not auth
        or auth.username is None
        or auth.password is None
        or not check_auth(auth.username, auth.password)
    ):
        return authenticate()

    file_to_delete = PDFFile.query.get_or_404(file_id)
    # Use disk_filename for removal from disk
    filepath = os.path.join(Config.UPLOAD_FOLDER, file_to_delete.disk_filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(file_to_delete)
    db.session.commit()

    flash(f"File {file_to_delete.filename} deleted successfully!", "success")
    return redirect(url_for("main.upload_file"))


@bp.route("/download/<int:file_id>")
def download_file(file_id: int) -> Response:
    """
    Serve a file for download using its unique ID.
    """
    file_record = PDFFile.query.get_or_404(file_id)
    return send_from_directory(Config.UPLOAD_FOLDER, file_record.disk_filename)


@bp.errorhandler(404)
def page_not_found(e: Exception) -> Any:
    """
    Render the 404 error page.
    """
    return render_template("404.html"), 404


@bp.errorhandler(500)
def internal_error(error: Exception) -> Any:
    """
    Render the 500 error page.
    """
    return render_template("500.html"), 500


@bp.route("/api")
def api() -> Response:
    """
    Provide a JSON API endpoint listing all uploaded PDF files.
    """
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


@bp.route("/robots.txt")
def robots_txt() -> Response:
    """
    Serve the content for robots.txt.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://www.uchurchmd.org/sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


__all__ = ["bp"]
