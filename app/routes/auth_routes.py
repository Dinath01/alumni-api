from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import UserReg, UserRes, UserLogin, TokenResponse 
from app.services.auth_service import create_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRes)
def register(user: UserReg, db: Session = Depends(get_db)):
    new_user = create_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, user)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return token