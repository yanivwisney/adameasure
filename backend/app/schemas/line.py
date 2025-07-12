from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .planting import Planting

class LineBase(BaseModel):
    name: str
    description: Optional[str] = None
    bed_id: int
    position: int
    length: Optional[float] = None
    width: Optional[float] = None
    spacing: Optional[float] = None
    is_active: bool = True

class LineCreate(LineBase):
    pass

class LineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    length: Optional[float] = None
    width: Optional[float] = None
    spacing: Optional[float] = None
    is_active: Optional[bool] = None

class Line(LineBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LineWithPlantings(Line):
    plantings: List['Planting'] = []
    
    class Config:
        from_attributes = True

LineWithPlantings.model_rebuild() 