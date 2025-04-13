# app/__init__.py
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from .config import Config
from .exceptions import register_error_handlers

# Initialize extensions once and reuse them throughout the app.
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")  # Adjust CORS settings for production

def create_app() -> Flask:
    """
    Application factory that creates and configures the Flask app instance.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static"),
    )
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # 마크다운 필터 추가 (YouTube 임베드 지원)
    @app.template_filter('markdown')
    def render_markdown(text):
        from markupsafe import Markup
        import markdown
        import re
        
        # YouTube 링크를 임베드로 변환
        def replace_youtube_links(text):
            # YouTube URL 패턴 (여러 형식 지원)
            patterns = [
                r'https?://(?:www\.)?youtube\.com/watch\?v=([\w-]+)(?:&\S*)?',
                r'https?://(?:www\.)?youtu\.be/([\w-]+)(?:\?\S*)?'
            ]
            
            for pattern in patterns:
                text = re.sub(
                    pattern,
                    r'<div class="ratio ratio-16x9 mb-3"><iframe src="https://www.youtube.com/embed/\1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>',
                    text
                )
            return text
            
        # YouTube 링크 치환 후 마크다운 변환
        processed_text = replace_youtube_links(text)
        return Markup(markdown.markdown(processed_text, extensions=['extra', 'nl2br']))

    # Register blueprints (e.g., main routes)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint.bp)

    # Register SocketIO events (for live chat functionality)
    from .sockets.livechat_manager import livechat_manager
    livechat_manager.register_events(socketio)

    # Register custom error handlers
    register_error_handlers(app)

    # Log configuration details
    logger = logging.getLogger(__name__)
    logger.info("App created with template folder: %s", app.template_folder)

    return app
