from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CropBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    scientific_name: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    growing_time_days: int = Field(..., gt=0)
    planting_depth_cm: Optional[float] = Field(None, ge=0)
    spacing_cm: Optional[float] = Field(None, gt=0)
    row_spacing_cm: Optional[float] = Field(None, gt=0)
    best_planting_seasons: Optional[List[int]] = None  # List of months (1-12)
    min_temperature_c: Optional[float] = None
    max_temperature_c: Optional[float] = None
    frost_tolerant: bool = False
    expected_yield_per_sqm: Optional[float] = Field(None, ge=0)
    harvest_window_days: Optional[int] = Field(None, ge=0)
    sun_requirements: Optional[str] = None
    water_requirements: Optional[str] = None
    soil_ph_min: Optional[float] = Field(None, ge=0, le=14)
    soil_ph_max: Optional[float] = Field(None, ge=0, le=14)
    market_price_per_kg: Optional[float] = Field(None, ge=0)
    storage_life_days: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    growing_notes: Optional[str] = None
    is_active: bool = True


class CropCreate(CropBase):
    pass


class CropUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    scientific_name: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    growing_time_days: Optional[int] = Field(None, gt=0)
    planting_depth_cm: Optional[float] = Field(None, ge=0)
    spacing_cm: Optional[float] = Field(None, gt=0)
    row_spacing_cm: Optional[float] = Field(None, gt=0)
    best_planting_seasons: Optional[List[int]] = None
    min_temperature_c: Optional[float] = None
    max_temperature_c: Optional[float] = None
    frost_tolerant: Optional[bool] = None
    expected_yield_per_sqm: Optional[float] = Field(None, ge=0)
    harvest_window_days: Optional[int] = Field(None, ge=0)
    sun_requirements: Optional[str] = None
    water_requirements: Optional[str] = None
    soil_ph_min: Optional[float] = Field(None, ge=0, le=14)
    soil_ph_max: Optional[float] = Field(None, ge=0, le=14)
    market_price_per_kg: Optional[float] = Field(None, ge=0)
    storage_life_days: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    growing_notes: Optional[str] = None
    is_active: Optional[bool] = None


class Crop(CropBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
