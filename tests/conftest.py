import pytest
from app import create_app
from src.models.todo import db


@pytest.fixture
def test_app():
    """
    Membuat instance Flask dengan in-memory DB untuk setiap test,
    lalu menghapus DB setelah test selesai.
    """
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    # Teardown
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()
