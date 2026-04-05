from pydantic import BaseModel, HttpUrl
from typing import Optional


class ProfileCreate(BaseModel):
    full_name: str
    bio: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    profile_image: Optional[str] = None


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    profile_image: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True