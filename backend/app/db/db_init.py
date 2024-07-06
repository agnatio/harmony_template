from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.db.db_auth import db_host, db_name, db_password, db_port, db_user

# Database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

TECH_DATABASE_URL = (
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
)

# Engine configuration
engine = create_engine(DATABASE_URL, echo=False)

# Base declarative class
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session
db_session = scoped_session(SessionLocal)

# Metadata from the Base class for schema generation
metadata = Base.metadata


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
