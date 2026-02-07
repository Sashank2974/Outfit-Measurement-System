"""
Measurement Model
SQLAlchemy model for measurements table with gender-specific fields
"""

from sqlalchemy import Column, String, DateTime, Integer, Numeric, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from config.database import Base

class Measurement(Base):
    """Measurement model with gender-specific fields"""
    __tablename__ = "measurements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    profile_id = Column(UUID(as_uuid=True), ForeignKey('measurement_profiles.id', ondelete='SET NULL'))
    gender = Column(String(10), nullable=False)  # 'male' or 'female'
    
    # Common measurements (in cm)
    height = Column(Numeric(6, 2))
    waist = Column(Numeric(6, 2))
    hip = Column(Numeric(6, 2))
    shoulder_width = Column(Numeric(6, 2))
    arm_length = Column(Numeric(6, 2))
    sleeve_length = Column(Numeric(6, 2))
    neck = Column(Numeric(6, 2))
    thigh = Column(Numeric(6, 2))
    calf = Column(Numeric(6, 2))
    
    # Male-specific measurements
    chest = Column(Numeric(6, 2))  # For males
    inseam = Column(Numeric(6, 2))
    outseam = Column(Numeric(6, 2))
    
    # Female-specific measurements
    bust = Column(Numeric(6, 2))  # For females
    under_bust = Column(Numeric(6, 2))
    
    # Confidence scores (0-100)
    height_confidence = Column(Numeric(5, 2))
    chest_bust_confidence = Column(Numeric(5, 2))
    waist_confidence = Column(Numeric(5, 2))
    hip_confidence = Column(Numeric(5, 2))
    overall_confidence = Column(Numeric(5, 2))
    
    # Metadata
    measurement_date = Column(DateTime, default=datetime.utcnow)
    processing_time_ms = Column(Integer)
    ai_model_version = Column(String(50))
    reference_object = Column(String(50))  # 'credit_card', 'a4_sheet', etc.
    
    # Status
    status = Column(String(20), default='completed')  # 'processing', 'completed', 'flagged', 'rejected'
    flagged_reason = Column(Text)
    admin_reviewed = Column(Boolean, default=False)
    admin_notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="measurements")
    profile = relationship("MeasurementProfile", back_populates="measurements")
    size_recommendations = relationship("SizeRecommendation", back_populates="measurement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Measurement {self.id} - {self.gender}>"
    
    def to_dict(self):
        """Convert measurement to dictionary"""
        return {
            "id": str(self.id),
            "gender": self.gender,
            "height": float(self.height) if self.height else None,
            "chest_bust": float(self.chest if self.gender == 'male' else self.bust) if (self.chest or self.bust) else None,
            "waist": float(self.waist) if self.waist else None,
            "hip": float(self.hip) if self.hip else None,
            "shoulder_width": float(self.shoulder_width) if self.shoulder_width else None,
            "overall_confidence": float(self.overall_confidence) if self.overall_confidence else None,
            "measurement_date": self.measurement_date.isoformat() if self.measurement_date else None,
            "status": self.status
        }


class MeasurementProfile(Base):
    """Measurement profile for managing multiple profiles per user"""
    __tablename__ = "measurement_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    profile_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    relationship_type = Column(String(50))  # 'self', 'spouse', 'child', etc.
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profiles")
    measurements = relationship("Measurement", back_populates="profile")
    
    def __repr__(self):
        return f"<MeasurementProfile {self.profile_name}>"


class SizeRecommendation(Base):
    """Size recommendation model"""
    __tablename__ = "size_recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    measurement_id = Column(UUID(as_uuid=True), ForeignKey('measurements.id', ondelete='CASCADE'), nullable=False)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('size_charts.id', ondelete='SET NULL'))
    
    # Recommended sizes
    general_size = Column(String(10))  # 'XS', 'S', 'M', 'L', 'XL', 'XXL'
    numeric_size = Column(String(10))  # '32', '34', '36', etc.
    
    # Size by region
    us_size = Column(String(10))
    uk_size = Column(String(10))
    eu_size = Column(String(10))
    asia_size = Column(String(10))
    
    # Fit preference
    fit_preference = Column(String(20))  # 'slim', 'regular', 'loose'
    
    # Confidence
    recommendation_confidence = Column(Numeric(5, 2))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    measurement = relationship("Measurement", back_populates="size_recommendations")
    
    def __repr__(self):
        return f"<SizeRecommendation {self.general_size}>"
