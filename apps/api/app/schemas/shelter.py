from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from datetime import time, datetime
from uuid import UUID


class ShelterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=500)
    lat: Decimal = Field(..., ge=-90, le=90)
    lon: Decimal = Field(..., ge=-180, le=180)
    neighborhood: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    hours: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = Field(None, max_length=500)
    requires_id: bool = False
    pet_friendly: bool = False
    ada_accessible: bool = False
    lgbtq_friendly: bool = False
    curfew_time: Optional[time] = None
    intake_notes: Optional[str] = Field(None, max_length=1000)
    languages: Optional[List[str]] = Field(None, max_items=10)


class ShelterCreate(ShelterBase):
    pass


class ShelterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    lat: Optional[Decimal] = Field(None, ge=-90, le=90)
    lon: Optional[Decimal] = Field(None, ge=-180, le=180)
    neighborhood: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    hours: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = Field(None, max_length=500)
    requires_id: Optional[bool] = None
    pet_friendly: Optional[bool] = None
    ada_accessible: Optional[bool] = None
    lgbtq_friendly: Optional[bool] = None
    curfew_time: Optional[time] = None
    intake_notes: Optional[str] = Field(None, max_length=1000)
    languages: Optional[List[str]] = Field(None, max_items=10)


class ShelterResponse(ShelterBase):
    id: UUID
    distance_km: Optional[float] = None

    class Config:
        from_attributes = True


class ShelterStatusBase(BaseModel):
    category: str = Field(..., regex="^(MEN|WOMEN|FAMILY|YOUTH|MIXED)$")
    beds_total: int = Field(..., ge=0, le=1000)
    beds_available: int = Field(..., ge=0, le=1000)
    status: str = Field(..., regex="^(OPEN|LIMITED|FULL|UNKNOWN)$")
    notes: Optional[str] = Field(None, max_length=500)

    @validator('beds_available')
    def beds_available_cannot_exceed_total(cls, v, values):
        if 'beds_total' in values and v > values['beds_total']:
            raise ValueError('beds_available cannot exceed beds_total')
        return v


class ShelterStatusCreate(ShelterStatusBase):
    shelter_id: UUID


class ShelterStatusUpdate(BaseModel):
    beds_total: Optional[int] = Field(None, ge=0, le=1000)
    beds_available: Optional[int] = Field(None, ge=0, le=1000)
    status: Optional[str] = Field(None, regex="^(OPEN|LIMITED|FULL|UNKNOWN)$")
    notes: Optional[str] = Field(None, max_length=500)


class ShelterStatusResponse(ShelterStatusBase):
    id: UUID
    shelter_id: UUID
    last_updated: datetime

    class Config:
        from_attributes = True
