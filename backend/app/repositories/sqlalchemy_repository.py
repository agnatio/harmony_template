# repositories/sqlalchemy_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.db_models import User
from app.repositories.user_repository_interface import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        db_user = self.db_session.query(User).filter(User.username == username).first()
        return db_user

    def create_user(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()

    def get_users(self) -> List[User]:
        return self.db_session.query(User).all()
