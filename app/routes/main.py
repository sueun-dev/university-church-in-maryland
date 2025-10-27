import os
import time
from datetime import datetime, timedelta
from typing import Any, List, Dict, Tuple
from flask import (
    render_template, Blueprint, request,
    redirect, url_for, flash, session, current_app, send_from_directory,
    abort, Response, jsonify
)
from werkzeug.utils import secure_filename
from flask.views import MethodView
import markdown
from markupsafe import Markup

from .. import db
from ..models import PDFFile, Post, ZoomLink, SiteContent, Message
from ..config import Config
from ..decorators import check_auth, requires_auth
from ..utils import allowed_file
from ..site_content_schema import iter_sections, get_field, get_default_for_key

# nl2br 필터 정의: 줄바꿈 문자를 HTML <br> 태그로 변환
def nl2br(value):
    if not value:
        return ""
    return Markup(value.replace('\n', '<br>'))

bp = Blueprint("main", __name__)


# 템플릿에서 사용할 콘텐츠 가져오기 함수
def get_content(key, default=None):
    """키를 기반으로 콘텐츠를 가져오는 유틸리티 함수"""
    content = SiteContent.query.filter_by(key=key).first()
    if content:
        return content.content
    if default is not None:
        return default
    return get_default_for_key(key)


def ensure_site_content_defaults() -> None:
    """Ensure every defined site content key exists in the database."""
    existing_items = {item.key: item for item in SiteContent.query.all()}
    changed = False

    for section in iter_sections():
        for field in section.fields:
            record = existing_items.get(field.key)
            if record is None:
                new_record = SiteContent(
                    key=field.key,
                    title=field.label,
                    content=field.default,
                )
                db.session.add(new_record)
                existing_items[field.key] = new_record
                changed = True
            elif record.title != field.label:
                record.title = field.label
                changed = True

    if changed:
        db.session.commit()


# 모든 템플릿에서 get_content 함수 사용 가능하도록 설정
@bp.context_processor
def inject_utility_functions():
    # get_content 함수와 함께 읽지 않은 메시지 수를 템플릿에 제공
    context = {
        "get_content": get_content
    }
    
    # 목사님이 로그인한 경우에만 읽지 않은 메시지 수 계산
    if session.get('is_pastor'):
        unread_count = Message.query.filter_by(is_read=False).count()
        context["unread_count"] = unread_count
    
    return context

# nl2br 필터 등록
@bp.app_template_filter('nl2br')
def nl2br_filter(s):
    return nl2br(s)

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Helper functions
def mark_new_files(files: List[PDFFile]) -> None:
    now = datetime.utcnow()
    for file in files:
        setattr(file, "is_new", (now - file.upload_date) <= timedelta(days=7))

def get_files_with_new_flag() -> List[PDFFile]:
    files = PDFFile.query.order_by(PDFFile.upload_date.desc()).all()
    mark_new_files(files)
    return files

def verify_auth() -> bool:
    auth = request.authorization
    return bool(auth and auth.username and auth.password and check_auth(auth.username, auth.password))

# Login attempt lockout logic
LOGIN_MAX_ATTEMPTS = 5
LOGIN_BLOCK_TIME = 1800
login_attempts_login: Dict[str, Tuple[int, float]] = {}

def is_ip_blocked_login(ip: str) -> bool:
    if ip in login_attempts_login:
        attempts, last_attempt = login_attempts_login[ip]
        return attempts >= LOGIN_MAX_ATTEMPTS and (time.time() - last_attempt) < LOGIN_BLOCK_TIME
    return False

def register_failed_login(ip: str) -> int:
    attempts, _ = login_attempts_login.get(ip, (0, 0))
    login_attempts_login[ip] = (attempts + 1, time.time())
    return LOGIN_MAX_ATTEMPTS - login_attempts_login[ip][0]

# Routes
@bp.route("/")
def index():
    zoom_link = ZoomLink.query.first()
    zoom_url = zoom_link.url if zoom_link else "https://us02web.zoom.us/j/89486134981#success"
    zoom_password = zoom_link.password if zoom_link and zoom_link.password else ""
    is_pastor = session.get('is_pastor', False)
    return render_template("index.html", zoom_url=zoom_url, zoom_password=zoom_password, is_pastor=is_pastor)


@bp.route("/pastor-chat")
@requires_auth()
def pastor_chat() -> str:
    return render_template("pastor_chat.html")

# General 게시글
class PostView(MethodView):
    def get(self) -> str:
        posts = Post.query.filter_by(category=None).order_by(Post.created_at.desc()).all()
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
        flash("게시글이 등록되었습니다.", "success")
        return redirect(url_for("main.read_posts"))

bp.add_url_rule("/read", view_func=PostView.as_view("read_posts"), methods=["GET", "POST"])

# Helper for categorized boards
def handle_post_category(category: str, template: str) -> Any:
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category=category).order_by(Post.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = pagination.items
    is_pastor = bool(session.get("is_pastor"))
    if request.method == "POST":
        if not is_pastor:
            flash("권한이 없습니다.", "danger")
            return redirect(request.url)
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        if not title or not content:
            flash("제목과 내용을 입력하세요.", "danger")
            return redirect(request.url)
        new_post = Post(title=title, content=content, category=category)
        db.session.add(new_post)
        db.session.commit()
        flash("게시글이 등록되었습니다.", "success")
        return redirect(request.url)
    return render_template(template, posts=posts, is_pastor=is_pastor, pagination=pagination, active_page=category)

@bp.route("/intro", methods=["GET", "POST"])
def intro():
    return handle_post_category("intro", "intro.html")

@bp.route("/sermons", methods=["GET", "POST"])
def sermons():
    return handle_post_category("sermons", "sermons.html")

@bp.route("/bible-study", methods=["GET", "POST"])
def bible_study():
    return handle_post_category("bible_study", "bible_study.html")

@bp.route("/church-life", methods=["GET", "POST"])
def church_life():
    return handle_post_category("church_life", "church_life.html")

@bp.route("/delete_post/<int:post_id>", methods=["POST"])
@requires_auth()
def delete_post(post_id: int) -> Any:
    """Delete a post based on its ID.

    Args:
        post_id: The ID of the post to delete.

    Returns:
        Redirect to the appropriate page after deletion.
    """
    # Require login to delete posts
    if not session.get("is_pastor"):
        flash("권한이 없습니다.", "danger")
        return redirect(url_for("main.index"))

    post = Post.query.get_or_404(post_id)
    category = post.category
    
    # Delete the post
    db.session.delete(post)
    db.session.commit()
    flash("게시글이 삭제되었습니다.", "success")
    
    # Determine which page to return to based on post category
    if category == "intro":
        return redirect(url_for("main.intro"))
    elif category == "sermons":
        return redirect(url_for("main.sermons"))
    elif category == "bible_study":
        return redirect(url_for("main.bible_study"))
    elif category == "church_life":
        return redirect(url_for("main.church_life"))
    else:
        return redirect(url_for("main.read_posts"))


@bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@requires_auth()
def edit_post(post_id: int) -> Any:
    """Edit a post based on its ID.

    Args:
        post_id: The ID of the post to edit.

    Returns:
        Edit form or redirect to the appropriate page after edit.
    """
    post = Post.query.get_or_404(post_id)
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if title and content:
            post.title = title
            post.content = content
            db.session.commit()
            flash("게시글이 성공적으로 수정되었습니다.", "success")
            
            # Determine which page to return to based on post category
            if post.category == "intro":
                return redirect(url_for("main.intro"))
            elif post.category == "sermons":
                return redirect(url_for("main.sermons"))
            elif post.category == "bible_study":
                return redirect(url_for("main.bible_study"))
            elif post.category == "church_life":
                return redirect(url_for("main.church_life"))
            else:
                return redirect(url_for("main.read_posts"))
        else:
            flash("제목과 내용을 모두 입력해주세요.", "danger")
    
    return render_template("edit_post.html", post=post)


@bp.route("/upload", methods=["GET", "POST"])
def upload_file() -> Any:
    """Handle file uploads."""
    # 세션 기반 인증 확인 - is_pastor 세션 값 확인
    is_pastor = session.get('is_pastor', False)
    
    if request.method == "POST":
        # 세션 기반 인증 또는 Basic Auth 둘 중 하나라도 통과하면 업로드 허용
        if not (is_pastor or verify_auth()):
            flash("파일 업로드를 위해 관리자 권한이 필요합니다.", "warning")
            return redirect(url_for('main.login', next=request.path))
            
        try:
            if "file_input" not in request.files:
                flash("파일이 선택되지 않았습니다.", "danger")
                return redirect(request.url)
                
            file = request.files["file_input"]
            original_filename = file.filename or ""
            
            if not original_filename:
                flash("파일이 선택되지 않았습니다.", "danger")
                return redirect(request.url)
                
            if not allowed_file(original_filename):
                flash("허용되지 않는 파일 형식입니다.", "danger")
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
            
            flash(f"파일 '{original_filename}'이 성공적으로 업로드되었습니다.", "success")
            files = get_files_with_new_flag()
            return render_template("upload.html", files=files, success=True)
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"파일 업로드 중 오류 발생: {str(e)}")
            flash(f"파일 업로드 중 오류가 발생했습니다: {str(e)}", "danger")
            return redirect(request.url)
            
    # GET 요청 처리
    files = get_files_with_new_flag()
    return render_template("upload.html", files=files, success=False, is_pastor=is_pastor)


@bp.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id: int) -> Any:
    """Delete a file record and remove the file from disk."""
    # 세션 기반 인증 확인 - is_pastor 세션 값 확인
    is_pastor = session.get('is_pastor', False)
    
    # 세션 기반 인증 또는 Basic Auth 둘 중 하나라도 통과하면 삭제 허용
    if not (is_pastor or verify_auth()):
        flash("파일 삭제를 위해 관리자 권한이 필요합니다.", "warning")
        return redirect(url_for('main.login', next=request.path))
        
    try:
        file_to_delete = PDFFile.query.get_or_404(file_id)
        filename = file_to_delete.filename  # 삭제 전 파일명 저장
        
        # 디스크에서 파일 삭제
        filepath = os.path.join(Config.UPLOAD_FOLDER, file_to_delete.disk_filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            
        # DB에서 레코드 삭제
        db.session.delete(file_to_delete)
        db.session.commit()
        
        flash(f"파일 '{filename}'이 성공적으로 삭제되었습니다.", "success")
        return redirect(url_for("main.upload_file"))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"파일 삭제 중 오류 발생: {str(e)}")
        flash(f"파일 삭제 중 오류가 발생했습니다: {str(e)}", "danger")
        return redirect(url_for("main.upload_file"))

@bp.route("/update-zoom-link", methods=["POST"])
@requires_auth()
def update_zoom_link():
    new_url = request.form.get("zoom_url", "").strip()
    new_password = request.form.get("zoom_password", "").strip()
    if new_url:
        zoom_link = ZoomLink.query.first()
        if zoom_link:
            zoom_link.url = new_url
            zoom_link.password = new_password if new_password else None
        else:
            zoom_link = ZoomLink(url=new_url, password=new_password if new_password else None)
            db.session.add(zoom_link)
        db.session.commit()
        flash("Zoom 링크가 성공적으로 변경되었습니다.", "success")
    else:
        flash("올바른 URL을 입력해주세요.", "danger")
    return redirect(url_for("main.index"))


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

@bp.route('/about')
def about():
    return render_template('about.html', active_page='about')


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


@bp.route("/manage-content", methods=["GET", "POST"])
@requires_auth()
def manage_content() -> Any:
    """새로운 콘텐츠 관리 페이지."""
    ensure_site_content_defaults()

    if request.method == "POST":
        key = (request.form.get("key") or "").strip()
        new_value = request.form.get("content") or ""

        field_meta = get_field(key) if key else None
        if field_meta is None:
            flash("수정할 항목을 찾을 수 없습니다.", "danger")
            return redirect(url_for("main.manage_content"))

        content_record = SiteContent.query.filter_by(key=key).first()
        if content_record is None:
            content_record = SiteContent(
                key=key,
                title=field_meta.label,
                content=new_value,
            )
            db.session.add(content_record)
        else:
            content_record.title = field_meta.label
            content_record.content = new_value

        db.session.commit()
        flash(f"'{field_meta.label}' 항목이 저장되었습니다.", "success")
        return redirect(url_for("main.manage_content", _anchor=key))

    existing_items = {item.key: item for item in SiteContent.query.all()}
    sections: List[Dict[str, Any]] = []
    for section in iter_sections():
        section_fields = []
        for field in section.fields:
            record = existing_items.get(field.key)
            section_fields.append(
                {
                    "meta": field,
                    "value": record.content if record else field.default,
                    "updated_at": record.updated_at if record else None,
                }
            )
        sections.append(
            {
                "id": section.id,
                "title": section.title,
                "description": section.description,
                "fields": section_fields,
            }
        )

    return render_template("manage_content.html", sections=sections)


# 메시지 관련 라우트
@bp.route("/message", methods=["GET", "POST"])
def send_message():
    """메시지 남기기"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip() or None
        subject = request.form.get("subject", "").strip()
        content = request.form.get("content", "").strip()
        
        if not name or not subject or not content:
            flash("이름, 제목, 내용은 필수 입력 항목입니다.", "danger")
            return redirect(url_for("main.send_message"))
            
        message = Message(name=name, email=email, subject=subject, content=content)
        db.session.add(message)
        db.session.commit()
        
        flash("메시지가 성공적으로 전송되었습니다. 목사님께서 확인 후 연락드릴 것입니다.", "success")
        return redirect(url_for("main.index"))
        
    return render_template("message.html")


@bp.route("/messages")
@requires_auth()
def messages():
    """메시지 목록 보기 (관리자 전용)"""
    messages_list = Message.query.order_by(Message.created_at.desc()).all()
    unread_count = Message.query.filter_by(is_read=False).count()
    
    return render_template("message_list.html", messages_list=messages_list, unread_count=unread_count)


@bp.route("/message/<int:message_id>")
@requires_auth()
def view_message(message_id):
    """메시지 상세 보기 (관리자 전용)"""
    message = Message.query.get_or_404(message_id)
    
    # 읽음 상태로 변경
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template("view_message.html", message=message)


@bp.route("/message/delete/<int:message_id>", methods=["POST"])
@requires_auth()
def delete_message(message_id):
    """메시지 삭제 (관리자 전용)"""
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    
    flash("메시지가 삭제되었습니다.", "success")
    return redirect(url_for("main.messages"))
