import pytest
from app import create_app, get_db


@pytest.fixture
def app(tmp_path):
    """Create and configure a clean Flask application instance for each test."""
    db_path = tmp_path / "test_tasks.db"

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(db_path),
            "SECRET_KEY": "test-secret-key",
        }
    )

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
