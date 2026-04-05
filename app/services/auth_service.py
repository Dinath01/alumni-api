from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserReg, UserLogin
from passlib.context import CryptContext
from app.core.security import hash_password,verify_password, create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user_data: UserReg):
    #if user already exists
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

def authenticate_user(db: Session, user_data: UserLogin):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        return None

    if not verify_password(user_data.password, user.password_hash):
        return None

    return user


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