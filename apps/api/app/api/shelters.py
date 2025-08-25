from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from decimal import Decimal
from uuid import UUID

from app.database import get_db
from app.models import Shelter, ShelterStatus
from app.schemas.shelter import (
    ShelterResponse, 
    ShelterStatusResponse,
    ShelterStatusUpdate
)
from app.services.availability import apply_conservatism_rule
from app.services.geo import calculate_distance, get_neighborhood

router = APIRouter()


@router.get("/", response_model=List[ShelterResponse])
async def get_shelters(
    near: Optional[str] = Query(None, description="lat,lon coordinates"),
    radius_km: float = Query(10.0, ge=0.1, le=50.0),
    open: Optional[bool] = Query(None, description="Filter by open status"),
    category: Optional[str] = Query(None, regex="^(MEN|WOMEN|FAMILY|YOUTH|MIXED)$"),
    neighborhood: Optional[str] = Query(None),
    pet_friendly: Optional[bool] = Query(None),
    ada_accessible: Optional[bool] = Query(None),
    lgbtq_friendly: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Get shelters with optional filtering and distance sorting
    """
    query = select(Shelter).options(selectinload(Shelter.statuses))
    
    # Apply filters
    if neighborhood:
        query = query.where(Shelter.neighborhood.ilike(f"%{neighborhood}%"))
    
    if pet_friendly is not None:
        query = query.where(Shelter.pet_friendly == pet_friendly)
    
    if ada_accessible is not None:
        query = query.where(Shelter.ada_accessible == ada_accessible)
    
    if lgbtq_friendly is not None:
        query = query.where(Shelter.lgbtq_friendly == lgbtq_friendly)
    
    result = await db.execute(query)
    shelters = result.scalars().all()
    
    # Apply conservatism rule to statuses
    for shelter in shelters:
        for status in shelter.statuses:
            apply_conservatism_rule(status)
    
    # Filter by category and open status
    if category or open is not None:
        filtered_shelters = []
        for shelter in shelters:
            matching_statuses = [
                s for s in shelter.statuses
                if (category is None or s.category == category) and
                   (open is None or (open and s.status in ['OPEN', 'LIMITED']) or 
                    (not open and s.status in ['FULL', 'UNKNOWN']))
            ]
            if matching_statuses:
                shelter.statuses = matching_statuses
                filtered_shelters.append(shelter)
        shelters = filtered_shelters
    
    # Calculate distances and sort if coordinates provided
    if near:
        try:
            lat_str, lon_str = near.split(',')
            lat, lon = Decimal(lat_str.strip()), Decimal(lon_str.strip())
            
            for shelter in shelters:
                shelter.distance_km = calculate_distance(lat, lon, shelter.lat, shelter.lon)
            
            # Sort by distance
            shelters.sort(key=lambda x: x.distance_km or float('inf'))
            
            # Filter by radius
            shelters = [s for s in shelters if s.distance_km <= radius_km]
            
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=400,
                detail="Invalid coordinates format. Use 'lat,lon'"
            )
    
    return shelters


@router.get("/{shelter_id}", response_model=ShelterResponse)
async def get_shelter(
    shelter_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific shelter by ID
    """
    query = select(Shelter).options(selectinload(Shelter.statuses)).where(Shelter.id == shelter_id)
    result = await db.execute(query)
    shelter = result.scalar_one_or_none()
    
    if not shelter:
        raise HTTPException(status_code=404, detail="Shelter not found")
    
    # Apply conservatism rule
    for status in shelter.statuses:
        apply_conservatism_rule(status)
    
    return shelter


@router.get("/{shelter_id}/status", response_model=List[ShelterStatusResponse])
async def get_shelter_status(
    shelter_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get status for all categories of a specific shelter
    """
    query = select(ShelterStatus).where(ShelterStatus.shelter_id == shelter_id)
    result = await db.execute(query)
    statuses = result.scalars().all()
    
    if not statuses:
        raise HTTPException(status_code=404, detail="Shelter status not found")
    
    # Apply conservatism rule
    for status in statuses:
        apply_conservatism_rule(status)
    
    return statuses
