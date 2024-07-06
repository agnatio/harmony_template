# backend/app/db/test_db_create.py

import sqlalchemy
from sqlalchemy import text, exc
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.db.db_init import engine, metadata
from app.db.db_auth import db_host, db_name, db_password, db_port, db_user
import asyncio

TEST_DATABASE_NAME = "test_db"  # Replace with your test database name


async def async_create_test_database():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_test_database)


async def async_create_test_tables():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_tables)


def create_test_database():
    # Connect to the default 'postgres' database to create the new database
    default_engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres",
        echo=False,
    )
    with default_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        # Attempt to create the new test database (if it doesn't exist)
        try:
            conn.execute(text(f"CREATE DATABASE {TEST_DATABASE_NAME}"))
            print(f"Test Database {TEST_DATABASE_NAME} created successfully.")
        except sqlalchemy.exc.ProgrammingError as e:
            print(f"Test Database {TEST_DATABASE_NAME} already exists. Error: {e}")


def drop_test_database():
    # Connect to the default database to drop the test database
    default_engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres",
        echo=False,
    )
    with default_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        # Attempt to drop the test database
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DATABASE_NAME}"))
            print(f"Test Database {TEST_DATABASE_NAME} dropped successfully.")
        except exc.SQLAlchemyError as e:
            print(f"Error dropping test database {TEST_DATABASE_NAME}. Error: {e}")


def create_tables():
    # Use the engine from db_init.py to create tables in the test database
    test_engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{TEST_DATABASE_NAME}",
        echo=False,
    )
    with test_engine.begin() as conn:
        metadata.create_all(bind=conn)
        print("Tables created successfully in test database.")
