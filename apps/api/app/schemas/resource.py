from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from uuid import UUID


class ResourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    type: str = Field(..., regex="^(FOOD|SHOWER|HEALTH|LEGAL|EMPLOYMENT|HYGIENE|COOLING|WARMING|SAFE_PARKING)$")
    address: str = Field(..., min_length=1, max_length=500)
    lat: Decimal = Field(..., ge=-90, le=90)
    lon: Decimal = Field(..., ge=-180, le=180)
    neighborhood: str = Field(..., min_length=1, max_length=100)
    hours: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=1000)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    type: Optional[str] = Field(None, regex="^(FOOD|SHOWER|HEALTH|LEGAL|EMPLOYMENT|HYGIENE|COOLING|WARMING|SAFE_PARKING)$")
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    lat: Optional[Decimal] = Field(None, ge=-90, le=90)
    lon: Optional[Decimal] = Field(None, ge=-180, le=180)
    neighborhood: Optional[str] = Field(None, min_length=1, max_length=100)
    hours: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = Field(None, max_length=1000)


class ResourceResponse(ResourceBase):
    id: UUID
    distance_km: Optional[float] = None

    class Config:
        from_attributes = True
