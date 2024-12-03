import pytest
import mongomock
import sys
import os

# Add 'backend' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from main import setup_app
from mongoengine import connect, disconnect

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = setup_app()
    app.config.update(
        TESTING=True,
        MONGODB_SETTINGS={
            'db': 'test_db',
            'host': 'localhost',
            'mongo_client_class': mongomock.MongoClient  # Use mongomock for testing
        },
    )
    with app.app_context():
        disconnect(alias='default')  # Disconnect any existing connections
        connect(
            'test_db',
            host='localhost',
            mongo_client_class=mongomock.MongoClient  # Use mongomock for testing
        )
        yield app
        disconnect(alias='default')  # Disconnect after the tests

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()