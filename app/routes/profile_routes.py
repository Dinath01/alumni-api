from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate, ProfileResponse
from app.services.auth_service import get_current_user
from app.services.profile_service import (
    create_profile,
    get_profile_by_user_id,
    update_profile,
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=ProfileResponse)
def create_my_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_profile = create_profile(db, current_user.id, profile)

    if not new_profile:
        raise HTTPException(status_code=400, detail="This Profile already exists")

    return new_profile


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = get_profile_by_user_id(db, current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="The Profile does not exist")

    return profile


@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_profile = update_profile(db, current_user.id, profile_data)

    if not updated_profile:
        raise HTTPException(status_code=404, detail="The Profile does not exist")

    return updated_profile