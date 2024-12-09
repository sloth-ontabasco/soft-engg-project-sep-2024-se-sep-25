import pytest
from src.app_factory import setup_app

@pytest.fixture()
def app():
    app = setup_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def _provide_app_context(app):
    with app.app_context():
        yield