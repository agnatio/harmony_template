from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.db.db_create import async_create_database, async_create_tables
from app.routers.auth import auth_router
from app.routers.users import users_router

import os


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        # Startup code
        await async_create_database()
        await async_create_tables()
        yield
    finally:
        pass


app = FastAPI(lifespan=app_lifespan)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

# Static files
dir_path = os.path.dirname(os.path.realpath(__file__))
app.mount(
    "/static", StaticFiles(directory=os.path.join(dir_path, "static")), name="static"
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
