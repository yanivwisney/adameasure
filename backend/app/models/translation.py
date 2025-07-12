from sqlalchemy import Column, Integer, String, Text, Boolean
from app.core.database import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(2), nullable=False, index=True)  # 'en', 'he'
    key = Column(String(255), nullable=False, index=True)
    value = Column(Text, nullable=False)
    category = Column(
        String(100), nullable=True, index=True
    )  # 'crops', 'farm_terms', 'ui'
    is_active = Column(Boolean, default=True)

    class Config:
        from_attributes = True
