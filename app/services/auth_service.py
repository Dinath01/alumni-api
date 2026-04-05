from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from app.core.security import (hash_password, verify_password, create_access_token, decode_access_token)

from app.db.database import get_db

from app.models.user import User
from app.schemas.user_schema import UserReg, UserLogin
from passlib.context import CryptContext

security = HTTPBearer()

#creation
def create_user(db: Session, user_data: UserReg):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        return None

    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#authentication
def authenticate_user(db: Session, user_data: UserLogin):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        return None

    if not verify_password(user_data.password, user.password_hash):
        return None

    return user

#login
def login_user(db: Session, user_data: UserLogin):
    user = authenticate_user(db, user_data)

    if not user:
        return None

    token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user