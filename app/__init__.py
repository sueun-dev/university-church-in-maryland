import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .exceptions import register_error_handlers

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()


def create_app() -> Flask:
    """
    Factory function to create and configure the Flask application.

    This function sets up the application configuration, initializes the database
    and migration utilities, registers blueprints, and configures global error handlers.

    Returns:
        Flask: A fully configured Flask application instance.
    """
    project_root: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app: Flask = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static"),
    )
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes.main import (
        bp as main_bp,
    )  # Local import to avoid circular dependencies

    app.register_blueprint(main_bp)

    # Register global error handlers
    register_error_handlers(app)

    print("Template folder:", app.template_folder)
    return app


__all__ = ["db", "migrate", "create_app"]
