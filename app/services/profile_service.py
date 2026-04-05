from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.schemas.profile_schema import ProfileCreate, ProfileUpdate


def create_profile(db: Session, user_id: int, profile_data: ProfileCreate):
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if existing_profile:
        return None

    new_profile = Profile(
        user_id=user_id,
        full_name=profile_data.full_name,
        bio=profile_data.bio,
        linkedin_url=str(profile_data.linkedin_url) if profile_data.linkedin_url else None,
        profile_image=profile_data.profile_image,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def update_profile(db: Session, user_id: int, profile_data: ProfileUpdate):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if not profile:
        return None

    update_data = profile_data.model_dump(exclude_unset=True)

    if "linkedin_url" in update_data and update_data["linkedin_url"] is not None:
        update_data["linkedin_url"] = str(update_data["linkedin_url"])

    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile