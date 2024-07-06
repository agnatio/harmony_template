from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import (
    HTTPException as StarletteHTTPException,
    RequestValidationError,
)

from sqlalchemy.orm import Session

from pydantic import BaseModel, ValidationError
from contextlib import asynccontextmanager

from app.db.db_create import async_create_database, async_create_tables
from app.db.db_init import get_db
from app.db.db_models import User as DBUser
from app.db.db_init import engine

from app.repositories.sqlalchemy_repository import SQLAlchemyUserRepository
from app.repositories.user_repository_interface import IUserRepository

from app.models.users import User, UserCreate

from app.routers.auth import auth_router
from app.routers.users import users_router

import os
import random

from icecream import ic


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        # Put your startup code here
        await async_create_database()
        await async_create_tables()
        app.include_router(auth_router, prefix="/auth", tags=["auth"])
        app.include_router(users_router, prefix="/users", tags=["users"])

        yield
    finally:
        pass


app = FastAPI(lifespan=app_lifespan)

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

dir_path = os.path.dirname(os.path.realpath(__file__))
app.mount(
    "/static", StaticFiles(directory=os.path.join(dir_path, "static")), name="static"
)


# # Dependency: User Repository
# def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
#     return SQLAlchemyUserRepository(db)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
