import sys
import os
import pytest
import sqlalchemy
from sqlalchemy import text, exc
from fastapi.testclient import TestClient

# Adjust the path to import app and test helpers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.main import app  # Import after setting the path
from app.db.db_init import (
    engine,
    SessionLocal,
    Base,
)  # Import SQLAlchemy engine and session setup
from tests.test_db_create import (
    async_create_test_database,
    async_create_test_tables,
    drop_test_database,
)


# Fixture to provide a FastAPI TestClient
@pytest.fixture
def client_fixture():
    with TestClient(app) as client:
        yield client


# Fixture to setup test database
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    import asyncio

    # Setup test database and tables
    asyncio.run(async_create_test_database())
    asyncio.run(async_create_test_tables())
    yield  # Yield control back to tests


# Fixture to provide a scoped session for database interactions
@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Fixture to cleanup test database after all tests
@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database():
    yield  # Let tests run
    drop_test_database()  # Cleanup test database after all tests
