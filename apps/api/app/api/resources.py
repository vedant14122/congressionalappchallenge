from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from decimal import Decimal

from app.database import get_db
from app.models import Resource
from app.schemas.resource import ResourceResponse
from app.services.geo import calculate_distance

router = APIRouter()


@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    type: Optional[str] = Query(None, regex="^(FOOD|SHOWER|HEALTH|LEGAL|EMPLOYMENT|HYGIENE|COOLING|WARMING|SAFE_PARKING)$"),
    near: Optional[str] = Query(None, description="lat,lon coordinates"),
    radius_km: float = Query(10.0, ge=0.1, le=50.0),
    neighborhood: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Get resources with optional filtering and distance sorting
    """
    query = select(Resource)
    
    if type:
        query = query.where(Resource.type == type)
    
    if neighborhood:
        query = query.where(Resource.neighborhood.ilike(f"%{neighborhood}%"))
    
    result = await db.execute(query)
    resources = result.scalars().all()
    
    # Calculate distances and sort if coordinates provided
    if near:
        try:
            lat_str, lon_str = near.split(',')
            lat, lon = Decimal(lat_str.strip()), Decimal(lon_str.strip())
            
            for resource in resources:
                resource.distance_km = calculate_distance(lat, lon, resource.lat, resource.lon)
            
            # Sort by distance
            resources.sort(key=lambda x: x.distance_km or float('inf'))
            
            # Filter by radius
            resources = [r for r in resources if r.distance_km <= radius_km]
            
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=400,
                detail="Invalid coordinates format. Use 'lat,lon'"
            )
    
    return resources
