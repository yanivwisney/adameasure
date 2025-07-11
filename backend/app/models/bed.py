from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Bed(Base):
    __tablename__ = "beds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    width = Column(Float, nullable=True)  # in meters
    length = Column(Float, nullable=True)  # in meters
    area = Column(Float, nullable=True)  # calculated area in square meters
    soil_type = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    farm = relationship("Farm", back_populates="beds")
    lines = relationship("Line", back_populates="bed", cascade="all, delete-orphan")
    plantings = relationship("Planting", back_populates="bed", cascade="all, delete-orphan")
    
    class Config:
        orm_mode = True 