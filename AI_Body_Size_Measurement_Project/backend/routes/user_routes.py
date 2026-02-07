"""
User Routes
API endpoints for user management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

from config.database import get_db
from models.user import User

router = APIRouter()

# Pydantic schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    gender: str  # 'male' or 'female'
    
class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    gender: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (password hashing should be added)
    new_user = User(
        email=user_data.email,
        password_hash=user_data.password,  # TODO: Hash password
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        gender=user_data.gender
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login")
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # TODO: Verify password hash
    # TODO: Generate JWT token
    
    return {
        "access_token": "dummy_token",
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db)):
    """Get current user profile"""
    # TODO: Get user from JWT token
    return {"message": "Current user endpoint"}

@router.put("/me", response_model=UserResponse)
async def update_user_profile(db: Session = Depends(get_db)):
    """Update user profile"""
    # TODO: Implement profile update
    return {"message": "Update profile endpoint"}
