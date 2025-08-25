from pydantic import BaseModel, Field
from typing import Optional, List, TypeVar, Generic
from decimal import Decimal

T = TypeVar('T')


class LocationQuery(BaseModel):
    lat: Decimal = Field(..., ge=-90, le=90, description="Latitude")
    lon: Decimal = Field(..., ge=-180, le=180, description="Longitude")
    radius_km: Optional[float] = Field(10.0, ge=0.1, le=50.0, description="Search radius in kilometers")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    per_page: int
    pages: int


class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: str
