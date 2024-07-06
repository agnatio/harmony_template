from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.db.db_create import async_create_database, async_create_tables
from app.db.db_init import get_db
from app.db.db_models import User as DBUser
from app.db.db_init import engine
from passlib.context import CryptContext

from app.repositories.sqlalchemy_repository import SQLAlchemyUserRepository
from app.repositories.user_repository_interface import IUserRepository

from app.utils.auth_utils import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)

from app.models.users import User, UserCreate

from app.dependencies.endpoint_dependencies import get_user_repository

users_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users_router.get("/hello")
async def hello_user():
    return {"message": "Hello, User!"}


@users_router.get("/{user_id}")
def read_user(
    user_id: int,
    user_repo: IUserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    user = user_repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user_repo: IUserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    user = user_repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_repo.delete_user(user_id)
    return {"message": "User deleted successfully"}


@users_router.get("/")
def get_all_users(
    user_repo: IUserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    users = user_repo.get_users()
    return users


@users_router.post("/")
def create_user(
    user: UserCreate,
    user_repo: IUserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
):
    hashed_password = pwd_context.hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_superuser=user.is_superuser,
    )
    created_user = user_repo.create_user(db_user)
    return created_user


@users_router.post("/register")
def register_user(
    user: UserCreate,
    user_repo: IUserRepository = Depends(get_user_repository),
):
    hashed_password = pwd_context.hash(user.password)
    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_superuser=False,
    )
    created_user = user_repo.create_user(db_user)
    return created_user
