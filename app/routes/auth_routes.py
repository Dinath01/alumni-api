from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import UserReg, UserRes, UserLogin, TokenResponse 
from app.models.user import User
from app.services.auth_service import create_user, login_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRes)
def register(user: UserReg, db: Session = Depends(get_db)):
    new_user = create_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="This email has already registered as an user!")

    return new_user


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, user)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return token

@router.get("/me", response_model=UserRes)
def read_current_user(current_user: User = Depends (get_current_user)):
    return current_user