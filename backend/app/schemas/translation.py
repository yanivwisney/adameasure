from pydantic import BaseModel
from typing import Optional, Dict, List

class TranslationBase(BaseModel):
    language: str
    key: str
    value: str
    category: Optional[str] = None
    is_active: bool = True

class TranslationCreate(TranslationBase):
    pass

class TranslationUpdate(BaseModel):
    value: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class Translation(TranslationBase):
    id: int
    
    class Config:
        orm_mode = True

class TranslationResponse(BaseModel):
    translations: Dict[str, str]  # key -> value mapping for a language

class BulkTranslationCreate(BaseModel):
    translations: List[TranslationCreate]

class BulkTranslationUpdate(BaseModel):
    updates: List[Dict[str, any]]  # List of {id, value, category, is_active} 