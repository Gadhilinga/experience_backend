import hashlib
import secrets

from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from models.user import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_token() -> str:
    return secrets.token_urlsafe(32)


def register_user(user_data, db: Session):
    existing_user = db.query(User).filter(
        or_(
            User.email == str(user_data.email),
            User.phone == user_data.mobile,
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email or mobile already registered.",
        )

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=str(user_data.email),
        phone=user_data.mobile,
        location=user_data.location,
        password_hash=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(login_data, db: Session):
    login_value = login_data.emailormbilenumber.strip()

    user = db.query(User).filter(
        or_(
            func.lower(User.email) == login_value.lower(),
            User.phone == login_value,
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    if user.password_hash != hash_password(login_data.password):
        raise HTTPException(
            status_code=401,
            detail="Password mismatch",
        )

    return {
        "success": True,
        "token": create_token(),
        "user": user,
    }


def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user