import pytest
import json
from airbnb.airbnb_db import get_db
from requests.auth import _basic_auth_str


def test_unknown_url(client, auth, app):
    response = client.get('/api/v1/unknown')
    assert response.status_code == 404
