from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(500), nullable=True)
    total_area = Column(Integer, nullable=True)  # in square meters
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    beds = relationship("Bed", back_populates="farm", cascade="all, delete-orphan")
    selling_schedules = relationship(
        "SellingSchedule", back_populates="farm", cascade="all, delete-orphan"
    )

    class Config:
        from_attributes = True
