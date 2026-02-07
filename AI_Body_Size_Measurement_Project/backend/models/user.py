"""
User Model
SQLAlchemy model for users table
"""

from sqlalchemy import Column, String, Boolean, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from config.database import Base

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(10), nullable=False)  # 'male' or 'female'
    date_of_birth = Column(Date)
    phone_number = Column(String(20))
    preferred_unit = Column(String(10), default='cm')  # 'cm' or 'inches'
    preferred_language = Column(String(10), default='en')
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    measurements = relationship("Measurement", back_populates="user", cascade="all, delete-orphan")
    profiles = relationship("MeasurementProfile", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"
