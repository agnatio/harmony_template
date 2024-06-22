# dependencies/user_dependency.py
from fastapi import Depends
from sqlalchemy.orm import Session
from db.db_init import SessionLocal, get_db
from repositories.sqlalchemy_repository import SQLAlchemyUserRepository
from repositories.user_repository_interface import IUserRepository


def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return SQLAlchemyUserRepository(db)
