# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from app.utils.auth_utils import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)
from app.db.db_init import get_db
from app.repositories.user_repository_interface import IUserRepository
from app.dependencies.endpoint_dependencies import get_user_repository
from app.models.auth_models import Token
from app.models.users import User
from pydantic import BaseModel

auth_router = APIRouter()


class UserLogin(BaseModel):
    username: str
    password: str


@auth_router.get("/test")
def check_router():
    return {"test": "test"}


@auth_router.post("/login", response_model=Token)
def login_for_access_token(
    user_login: UserLogin,
    db: Session = Depends(get_db),
    user_repo: IUserRepository = Depends(get_user_repository),
):
    username = user_login.username
    password = user_login.password
    print("login function")

    user = user_repo.get_user_by_username(username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=120)  # Adjust token expiry as needed
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print({"access_token": access_token, "token_type": "bearer"})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@auth_router.get("/checkauth")
async def check_auth(current_user: User = Depends(get_current_user)):
    return {"status": "Authenticated"}
