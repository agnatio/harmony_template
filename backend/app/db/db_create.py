import sqlalchemy
from sqlalchemy import text, exc
from app.db.db_init import (
    engine,
    DATABASE_URL,
    TECH_DATABASE_URL,
)  # Import the engine from db_init.py
from app.db.db_init import metadata  # Ensure this import matches your project structure
from app.db.db_auth import db_host, db_name, db_password, db_port, db_user
import asyncio


async def async_create_database():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None, create_database
    )  # Assuming create_database is your existing sync function


async def async_create_tables():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, create_tables)


def create_database():
    # Connect to the default 'postgres' database to create the new database
    default_engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres",  # Change to a default database
        echo=False,
    )
    with default_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        # Attempt to create the new database (if it doesn't exist)
        try:
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database {db_name} created successfully.")
        except sqlalchemy.exc.ProgrammingError as e:
            print(f"Database {db_name} already exists. Error: {e}")


def drop_database():
    # Connect to the default database to drop the target database
    default_engine = sqlalchemy.create_engine(
        TECH_DATABASE_URL,  # Make sure this URL points to the default database, not the one you intend to drop
        echo=False,
    )

    with default_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")

        # Attempt to drop the database
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
            print(f"Database {db_name} dropped successfully.")
        except exc.SQLAlchemyError as e:
            print(f"Error dropping database {db_name}. Error: {e}")


def create_tables():
    # Use the engine from db_init.py to create tables
    with engine.begin() as conn:
        metadata.create_all(bind=conn)
        print("Tables created successfully.")


if __name__ == "__main__":

    asyncio.run(async_create_database())  # Create the database asynchronously
    asyncio.run(async_create_tables())  # Create tables in the database asynchronously
