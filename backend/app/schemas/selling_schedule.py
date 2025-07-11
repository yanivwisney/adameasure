from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SellingScheduleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    first_selling_date: datetime
    selling_frequency_days: int = Field(..., gt=0)
    target_crops: Optional[List[int]] = None
    target_quantities: Optional[Dict[str, float]] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class SellingScheduleCreate(SellingScheduleBase):
    farm_id: int

class SellingScheduleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    first_selling_date: Optional[datetime] = None
    selling_frequency_days: Optional[int] = Field(None, gt=0)
    target_crops: Optional[List[int]] = None
    target_quantities: Optional[Dict[str, float]] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class SellingSchedule(SellingScheduleBase):
    id: int
    farm_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 