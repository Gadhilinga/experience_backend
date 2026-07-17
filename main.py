from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Experience Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.post(
    "/yatrivo/api/v1/auth/register",
    response_model=schemas.UserResponse,
    tags=["Authentication"],
    summary="User Registration",
    description="Register a new user using first name, last name, email, and phone number.",
    status_code=status.HTTP_201_CREATED,
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    "/yatrivo/api/v1/auth/users",
    response_model=List[schemas.UserResponse],
    tags=["Authentication"],
    summary="Get All Users",
    description="Retrieve a list of all registered users.",
)
def get_users(db: Session = Depends(get_db)):
    """
    Get all users.
    """
    users = db.query(models.User).all()
    return users


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
        raise HTTPException(status_code=404, detail="User not found")

    return user