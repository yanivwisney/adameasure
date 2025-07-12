from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HarvestBase(BaseModel):
    planting_id: int
    farm_id: int
    bed_id: int
    line_id: int
    crop_id: int
    harvest_date: datetime
    harvested_quantity: float = Field(..., gt=0, description="Harvested quantity in kg")
    quality_rating: Optional[int] = Field(None, ge=1, le=5, description="Quality rating 1-5")
    notes: Optional[str] = None
    weather_conditions: Optional[str] = None
    harvest_method: Optional[str] = None
    harvested_by: Optional[str] = None

class HarvestCreate(HarvestBase):
    pass

class HarvestUpdate(BaseModel):
    harvest_date: Optional[datetime] = None
    harvested_quantity: Optional[float] = Field(None, gt=0)
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None
    weather_conditions: Optional[str] = None
    harvest_method: Optional[str] = None
    harvested_by: Optional[str] = None
    is_complete: Optional[bool] = None

class HarvestResponse(HarvestBase):
    id: int
    days_early_late: Optional[int] = None
    expected_harvest_date: Optional[datetime] = None
    expected_yield: Optional[float] = None
    yield_percentage: Optional[float] = None
    is_complete: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class HarvestSummary(BaseModel):
    id: int
    crop_name: str
    bed_name: str
    line_name: str
    harvest_date: datetime
    harvested_quantity: float
    quality_rating: Optional[int]
    days_early_late: Optional[int]
    yield_percentage: Optional[float]
    is_complete: bool
    
    class Config:
        from_attributes = True 