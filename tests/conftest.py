# tests/conftest.py

import os
import tempfile
import pytest
from app import create_app, db


@pytest.fixture
def app():
    # Create a temporary file to serve as the test database.
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            # Override UPLOAD_FOLDER for tests if needed:
            "UPLOAD_FOLDER": os.path.join(app.root_path, "test_uploads"),
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
