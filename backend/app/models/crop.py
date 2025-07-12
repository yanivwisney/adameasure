from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    scientific_name = Column(String(255), nullable=True)
    category = Column(String(100), nullable=False)  # fruit, vegetable, herb, etc.

    # Growing information
    growing_time_days = Column(Integer, nullable=False)  # Days from planting to harvest
    planting_depth_cm = Column(Float, nullable=True)
    spacing_cm = Column(Float, nullable=True)  # Distance between plants
    row_spacing_cm = Column(Float, nullable=True)  # Distance between rows

    # Seasonal requirements
    best_planting_seasons = Column(
        JSON, nullable=True
    )  # List of months for optimal planting
    min_temperature_c = Column(Float, nullable=True)
    max_temperature_c = Column(Float, nullable=True)
    frost_tolerant = Column(Boolean, default=False)

    # Yield information
    expected_yield_per_sqm = Column(Float, nullable=True)  # kg per square meter
    harvest_window_days = Column(
        Integer, nullable=True
    )  # How long harvest can be delayed

    # Additional metadata
    sun_requirements = Column(
        String(50), nullable=True
    )  # full_sun, partial_shade, etc.
    water_requirements = Column(String(50), nullable=True)  # low, medium, high
    soil_ph_min = Column(Float, nullable=True)
    soil_ph_max = Column(Float, nullable=True)

    # Market information
    market_price_per_kg = Column(Float, nullable=True)
    storage_life_days = Column(Integer, nullable=True)

    # Notes and description
    description = Column(Text, nullable=True)
    growing_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    plantings = relationship(
        "Planting", back_populates="crop", cascade="all, delete-orphan"
    )

    class Config:
        from_attributes = True
