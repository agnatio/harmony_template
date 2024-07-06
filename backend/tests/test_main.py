# backend/tests/test_main.py
import pytest


@pytest.fixture
def client(client_fixture):
    return client_fixture


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
