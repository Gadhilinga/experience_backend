from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse,
)
from services.auth_service import (
    register_user,
    login_user,
    get_user_by_id,
)

router = APIRouter(
    prefix="/yatrivo/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(user, db)


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(payload, db)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_by_id(user_id, db)