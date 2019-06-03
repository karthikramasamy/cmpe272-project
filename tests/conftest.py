from os import environ as env
from os import path as path
from dotenv import load_dotenv

import pytest
from airbnb import create_app
from airbnb.airbnb_db import get_db, init_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    dotenv_path = path.join(path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # create the app with common test config
    app = create_app({
        'TESTING': True,
    })

    # create the database and load test data
    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
