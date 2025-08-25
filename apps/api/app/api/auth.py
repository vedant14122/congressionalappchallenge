from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.database import get_db
from app.models import Staff
from app.schemas.staff import StaffLogin, MagicLinkResponse, TokenResponse
from app.services.email import send_magic_link

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
MAGIC_LINK_SECRET = os.getenv("MAGIC_LINK_SECRET", "your-magic-link-secret-key")
MAGIC_LINK_BASE_URL = os.getenv("MAGIC_LINK_BASE_URL", "http://localhost:3000/verify")


@router.post("/magic-link", response_model=MagicLinkResponse)
async def send_magic_link_email(
    login: StaffLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Send magic link email to staff member
    """
    # Check if staff exists
    query = select(Staff).where(Staff.email == login.email)
    result = await db.execute(query)
    staff = result.scalar_one_or_none()
    
    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff member not found"
        )
    
    # Generate magic link token
    token_data = {
        "sub": str(staff.id),
        "email": staff.email,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    token = jwt.encode(token_data, MAGIC_LINK_SECRET, algorithm="HS256")
    magic_link = f"{MAGIC_LINK_BASE_URL}?token={token}"
    
    # Send email
    await send_magic_link(staff.email, magic_link)
    
    return MagicLinkResponse()


@router.post("/verify", response_model=TokenResponse)
async def verify_magic_link(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify magic link token and return JWT
    """
    try:
        payload = jwt.decode(token, MAGIC_LINK_SECRET, algorithms=["HS256"])
        staff_id = payload.get("sub")
        email = payload.get("email")
        
        if staff_id is None or email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        
        # Check if staff still exists
        query = select(Staff).where(Staff.id == staff_id, Staff.email == email)
        result = await db.execute(query)
        staff = result.scalar_one_or_none()
        
        if not staff:
            raise HTTPException(
                status_code=401,
                detail="Staff member not found"
            )
        
        # Generate JWT
        jwt_data = {
            "sub": str(staff.id),
            "email": staff.email,
            "role": staff.role,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        
        access_token = jwt.encode(jwt_data, JWT_SECRET, algorithm="HS256")
        
        return TokenResponse(access_token=access_token)
        
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
