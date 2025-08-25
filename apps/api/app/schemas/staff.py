from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID


class StaffBase(BaseModel):
    email: EmailStr
    shelter_id: Optional[UUID] = None
    role: str = Field("STAFF", regex="^(ADMIN|STAFF)$")
    locale: str = Field("en", regex="^(en|es|ko|hy|tl|zh)$")


class StaffCreate(StaffBase):
    pass


class StaffResponse(StaffBase):
    id: UUID

    class Config:
        from_attributes = True


class StaffLogin(BaseModel):
    email: EmailStr


class MagicLinkResponse(BaseModel):
    message: str = "Magic link sent to your email"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
