from pydantic import BaseModel, EmailStr, Field

#register
class UserReg(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

#response
class UserRes(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True