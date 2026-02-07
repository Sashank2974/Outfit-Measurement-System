"""
Measurement Routes
API endpoints for body measurements
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import base64

from config.database import get_db
from models.measurement import Measurement

router = APIRouter()

# Pydantic schemas
class MeasurementCreate(BaseModel):
    gender: str
    image_data: str  # Base64 encoded image
    reference_scale: float = 1.0

class MeasurementResponse(BaseModel):
    id: str
    gender: str
    height: float = None
    chest: float = None
    bust: float = None
    waist: float = None
    hip: float = None
    shoulder_width: float = None
    overall_confidence: float = None
    measurement_date: datetime
    status: str
    
    class Config:
        from_attributes = True

@router.post("/capture", response_model=MeasurementResponse, status_code=status.HTTP_201_CREATED)
async def capture_measurement(
    measurement_data: MeasurementCreate,
    db: Session = Depends(get_db)
):
    """Capture and process body measurement"""
    # TODO: Call AI service to process image
    # TODO: Save measurement to database
    # TODO: Generate size recommendation
    
    return {
        "message": "Measurement captured",
        "status": "processing"
    }

@router.get("/", response_model=List[MeasurementResponse])
async def get_user_measurements(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get user's measurement history"""
    # TODO: Get user from JWT token
    # measurements = db.query(Measurement).offset(skip).limit(limit).all()
    return []

@router.get("/{measurement_id}", response_model=MeasurementResponse)
async def get_measurement(
    measurement_id: str,
    db: Session = Depends(get_db)
):
    """Get specific measurement by ID"""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )
    
    return measurement

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(
    measurement_id: str,
    db: Session = Depends(get_db)
):
    """Delete a measurement"""
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )
    
    db.delete(measurement)
    db.commit()
    
    return None
