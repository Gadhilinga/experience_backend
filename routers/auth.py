from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from core.security import get_current_user

from core.database import get_db
from core.security import verify_token
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


def extract_token_from_request(request: Request) -> str | None:
    authorization = request.headers.get("authorization") or request.headers.get("Authorization")
    if authorization:
        token = authorization
        if token.lower().startswith("bearer "):
            return token[7:].strip()
        if token.lower().startswith("token "):
            return token[5:].strip()
        return token.strip()

    token = request.query_params.get("token")
    if token:
        return str(token).strip()

    return None


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
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token_user_id = current_user.get("sub")

    if token_user_id is None or str(token_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this profile",
        )

    return get_user_by_id(user_id, db)
from schemas.user import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
)
from services.auth_service import (
    register_user,
    login_user,
    get_user_by_id,
    logout_user,
)

# ...

@router.post(
    "/logout",
    summary="Logout user",
)
def logout(request: LogoutRequest):
    if request.user_id <= 0 or not request.access_token:
        raise HTTPException(status_code=400, detail="user_id and access_token are required")

    logout_user(request.user_id, request.access_token)
    return {"message": "Logged out successfully"}    
