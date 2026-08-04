from fastapi import HTTPException
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from core.security import create_access_token, hash_password, verify_password
from models.user import User


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

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Password mismatch",
        )

    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
    })

    return {
        "success": True,
        "token": token,
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