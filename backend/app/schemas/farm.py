from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
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
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class FarmWithBeds(Farm):
    beds: List["Bed"] = []

    class Config:
        from_attributes = True


# Import Bed after the class definition to avoid circular imports
from .bed import Bed

FarmWithBeds.model_rebuild()
