from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserReg
from passlib.context import CryptContext

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