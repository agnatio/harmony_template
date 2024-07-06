# repositories/in_memory_repository.py
from typing import List
from db.db_models import User
from repositories.user_repository_interface import IUserRepository


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = []
        self.counter = 1

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def create_user(self, user: User) -> User:
        user.id = self.counter
        self.counter += 1
        self.users.append(user)
        return user

    def get_users(self) -> List[User]:
        return self.users
