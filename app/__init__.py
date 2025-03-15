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
