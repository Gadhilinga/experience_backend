import hashlib
import logging
import secrets
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import func, inspect, or_, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_token() -> str:
    return secrets.token_urlsafe(32)


logger = logging.getLogger(__name__)

def ensure_user_columns() -> None:
    try:
        inspector = inspect(engine)
    except (OperationalError, Exception) as exc:
        logger.warning("Database unavailable during startup; skipping schema initialization: %s", exc)
        return

    try:
        if "users" not in inspector.get_table_names():
            models.Base.metadata.create_all(bind=engine)
            return

        columns = {column["name"] for column in inspector.get_columns("users")}
        if "location" not in columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN location VARCHAR"))

        if "password_hash" not in columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR"))

        models.Base.metadata.create_all(bind=engine)
    except (OperationalError, Exception) as exc:
        logger.warning("Unable to initialize database schema: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_user_columns()
    yield


app = FastAPI(
    title="Experience Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


@app.post(
    "/yatrivo/api/v1/auth/register",
    response_model=schemas.UserResponse,
    tags=["Authentication"],
    summary="User Registration",
    description="Register a new user using first name, last name, email, mobile, location, and password.",
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """

    existing_user = db.query(models.User).filter(
        or_(models.User.email == str(user.email), models.User.phone == user.mobile)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or mobile already registered.")

    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=str(user.email),
        phone=user.mobile,
        location=user.location,
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/yatrivo/api/v1/auth/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):

    login_value = payload.emailormbilenumber.strip()

    print("Login value:", login_value)
    print("Input password:", payload.password)
    print("Input hash:", hash_password(payload.password))

    user = db.query(models.User).filter(
        or_(
            func.lower(models.User.email) == login_value.lower(),
            models.User.phone == login_value,
        )
    ).first()

    print("User found:", user)

    if user:
        print("DB email:", user.email)
        print("DB phone:", user.phone)
        print("DB hash:", user.password_hash)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.password_hash != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Password mismatch")

    return {
        "success": True,
        "token": create_token(),
        "user": user,
    }

@app.get(
    "/yatrivo/api/v1/auth/users/{user_id}",
    response_model=schemas.UserResponse,
    tags=["Authentication"],
    summary="Get User By ID",
    description="Retrieve a single registered user by their ID.",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user