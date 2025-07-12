from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .bed import Bed


class FarmBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    total_area: Optional[int] = None
    is_active: bool = True


class FarmCreate(FarmBase):
    pass


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    total_area: Optional[int] = None
    is_active: Optional[bool] = None


class Farm(FarmBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FarmWithBeds(Farm):
    beds: List["Bed"] = []

    class Config:
        from_attributes = True


FarmWithBeds.model_rebuild()
