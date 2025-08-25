from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv
from datetime import datetime

from app.database import get_db
from app.api import shelters, resources, auth, staff, alerts, push
from app.services.availability import apply_conservatism_rule

load_dotenv()

app = FastAPI(
    title="ShelterLink API",
    description="LA County shelter and resource finder API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8081").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(shelters.router, prefix="/shelters", tags=["shelters"])
app.include_router(resources.router, prefix="/resources", tags=["resources"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(push.router, prefix="/push", tags=["push"])


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "ShelterLink API",
        "version": "1.0.0",
        "docs": "/docs",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.post("/feedback", tags=["feedback"])
async def submit_feedback(
    message: str,
    context: str = "",
    db: AsyncSession = Depends(get_db)
):
    """
    Submit user feedback (anonymous)
    """
    # In a real implementation, you might want to store this in a database
    # For now, we'll just log it
    print(f"Feedback received: {message}")
    if context:
        print(f"Context: {context}")
    
    return {"message": "Feedback received", "status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
