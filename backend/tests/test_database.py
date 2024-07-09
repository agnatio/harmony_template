import pytest
from sqlalchemy.orm import Session
from app.db.db_models import User  # Replace with your SQLAlchemy models
from app.main import app  # Import app if needed for integration tests

# Remove the 'db' fixture definition
# pytest.fixture
# def db():
#     # Setup and teardown for the database if necessary
#     yield
#     # Teardown code if needed


# Use 'db_session' fixture for database interaction
def test_create_user(db_session: Session):
    user = User(username="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None  # Ensure user was persisted and has an ID


def test_get_user(db_session: Session):
    # Example of querying a user from the database
    user = db_session.query(User).filter_by(username="Test User").first()
    assert user is not None
    assert user.email == "test@example.com"


def test_delete_user(db_session: Session):
    user = db_session.query(User).filter_by(username="Test User").first()
    assert user is not None  # Ensure the user exists before trying to delete

    # Delete the user
    db_session.delete(user)
    db_session.commit()

    # Verify the user has been deleted
    deleted_user = db_session.query(User).filter_by(username="Test User").first()
    assert deleted_user is None  # The user should no longer exist in the database
