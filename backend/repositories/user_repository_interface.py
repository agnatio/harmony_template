# repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from db.db_models import User


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_users(self) -> List[User]:
        pass

    @abstractmethod
    def delete_user(self):
        pass
