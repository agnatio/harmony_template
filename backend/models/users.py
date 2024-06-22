# models/user.py
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str
    is_superuser: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
