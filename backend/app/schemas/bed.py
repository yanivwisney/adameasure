from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
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
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class BedWithLines(Bed):
    lines: List["Line"] = []

    class Config:
        from_attributes = True


# Import Line after the class definition to avoid circular imports
from .line import Line
BedWithLines.model_rebuild()
