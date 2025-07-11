from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Harvest(Base):
    __tablename__ = "harvests"
    
    id = Column(Integer, primary_key=True, index=True)
    planting_id = Column(Integer, ForeignKey("plantings.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    
    # Harvest data
    harvest_date = Column(DateTime, nullable=False)
    harvested_quantity = Column(Float, nullable=False)  # in kg
    quality_rating = Column(Integer, nullable=True)  # 1-5 scale
    notes = Column(Text, nullable=True)
    
    # Timing analysis
    days_early_late = Column(Integer, nullable=True)  # Positive = early, Negative = late
    expected_harvest_date = Column(DateTime, nullable=True)
    
    # Yield analysis
    expected_yield = Column(Float, nullable=True)  # in kg
    yield_percentage = Column(Float, nullable=True)  # actual vs expected
    
    # Metadata
    weather_conditions = Column(String(100), nullable=True)
    harvest_method = Column(String(50), nullable=True)  # manual, machine, etc.
    harvested_by = Column(String(100), nullable=True)
    
    # Status
    is_complete = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    planting = relationship("Planting", back_populates="harvests")
    farm = relationship("Farm")
    bed = relationship("Bed")
    line = relationship("Line")
    crop = relationship("Crop")
    
    class Config:
        orm_mode = True 