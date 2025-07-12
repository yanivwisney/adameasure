from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class SellingSchedule(Base):
    __tablename__ = "selling_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    
    # Schedule configuration
    name = Column(String(255), nullable=False)
    first_selling_date = Column(DateTime(timezone=True), nullable=False)
    selling_frequency_days = Column(Integer, nullable=False)  # Every X days
    is_active = Column(Boolean, default=True)
    
    # Target information
    target_crops = Column(JSON, nullable=True)  # List of crop IDs to focus on
    target_quantities = Column(JSON, nullable=True)  # Target quantities per selling date
    
    # Notes and description
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    farm = relationship("Farm", back_populates="selling_schedules")
    
    class Config:
        from_attributes = True 