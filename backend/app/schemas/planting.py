from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PlantingBase(BaseModel):
    crop_id: int
    farm_id: int
    bed_id: int
    line_id: int
    quantity: int
    planted_date: datetime
    expected_harvest_date: Optional[datetime] = None
    actual_harvest_date: Optional[datetime] = None
    harvested_quantity: Optional[float] = None
    notes: Optional[str] = None
    is_active: bool = True


class PlantingCreate(PlantingBase):
    pass


class PlantingUpdate(BaseModel):
    quantity: Optional[int] = None
    expected_harvest_date: Optional[datetime] = None
    actual_harvest_date: Optional[datetime] = None
    harvested_quantity: Optional[float] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class Planting(PlantingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlantingSuggestion(BaseModel):
    crop_id: int
    crop_name: str
    bed_id: int
    bed_name: str
    planting_date: datetime
    expected_harvest_date: datetime
    suggested_quantity: int
    priority: float

    class Config:
        from_attributes = True


class PlantingScheduleRequest(BaseModel):
    farm_id: int
    selling_schedule_id: int
    target_date: datetime
    frequency_days: int = Field(..., gt=0)
