from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .line import Line

class BedBase(BaseModel):
    name: str
    description: Optional[str] = None
    farm_id: int
    width: Optional[float] = None
    length: Optional[float] = None
    area: Optional[float] = None
    soil_type: Optional[str] = None
    is_active: bool = True

class BedCreate(BedBase):
    pass

class BedUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    width: Optional[float] = None
    length: Optional[float] = None
    area: Optional[float] = None
    soil_type: Optional[str] = None
    is_active: Optional[bool] = None

class Bed(BedBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BedWithLines(Bed):
    lines: List['Line'] = []
    
    class Config:
        from_attributes = True

BedWithLines.model_rebuild() 