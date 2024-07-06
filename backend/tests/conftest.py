# backend/tests/conftest.py
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Adjust the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from main import app  # Import after setting the path

client = TestClient(app)


@pytest.fixture
def client_fixture():
    return client
