"""
Admin Routes
API endpoints for admin operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from config.database import get_db
from models.user import User
from models.measurement import Measurement

router = APIRouter()

# Pydantic schemas
class AdminStats(BaseModel):
    total_users: int
    total_measurements: int
    avg_confidence: float
    flagged_measurements: int

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    # TODO: Check admin authorization
    
    total_users = db.query(User).count()
    total_measurements = db.query(Measurement).count()
    
    return {
        "total_users": total_users,
        "total_measurements": total_measurements,
        "avg_confidence": 0.0,
        "flagged_measurements": 0
    }

@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    # TODO: Check admin authorization
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/measurements/flagged")
async def get_flagged_measurements(db: Session = Depends(get_db)):
    """Get flagged measurements for review"""
    # TODO: Check admin authorization
    flagged = db.query(Measurement).filter(Measurement.status == 'flagged').all()
    return flagged

@router.put("/measurements/{measurement_id}/review")
async def review_measurement(
    measurement_id: str,
    db: Session = Depends(get_db)
):
    """Review and approve/reject measurement"""
    # TODO: Check admin authorization
    # TODO: Update measurement status
    return {"message": "Measurement reviewed"}
