from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Line(Base):
    __tablename__ = "lines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)
    position = Column(Integer, nullable=False)  # Line position within the bed (1, 2, 3, etc.)
    length = Column(Float, nullable=True)  # Length of the line in meters
    width = Column(Float, nullable=True)  # Width of the line in meters
    spacing = Column(Float, nullable=True)  # Spacing between plants in the line (cm)
    area = Column(Float, nullable=True)  # calculated area in square meters
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bed = relationship("Bed", back_populates="lines")
    plantings = relationship("Planting", back_populates="line", cascade="all, delete-orphan")
    
    class Config:
        from_attributes = True 