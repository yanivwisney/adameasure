from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Planting(Base):
    __tablename__ = "plantings"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=False)
    quantity = Column(Integer, nullable=False)  # Number of plants planted
    planted_date = Column(DateTime, nullable=False)
    expected_harvest_date = Column(DateTime, nullable=True)
    actual_harvest_date = Column(DateTime, nullable=True)
    harvested_quantity = Column(Float, nullable=True)  # in kg
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    crop = relationship("Crop", back_populates="plantings")
    farm = relationship("Farm")
    bed = relationship("Bed", back_populates="plantings")
    line = relationship("Line", back_populates="plantings")
    harvests = relationship("Harvest", back_populates="planting")

    class Config:
        from_attributes = True
