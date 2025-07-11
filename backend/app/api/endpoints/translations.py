from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.core.database import get_db
from app.models.translation import Translation
from app.schemas.translation import (
    TranslationCreate, 
    TranslationUpdate, 
    Translation as TranslationSchema,
    TranslationResponse,
    BulkTranslationCreate,
    BulkTranslationUpdate
)

router = APIRouter()

@router.get("/{language}", response_model=TranslationResponse)
def get_translations(language: str, db: Session = Depends(get_db)):
    """Get all translations for a specific language"""
    translations = db.query(Translation).filter(
        Translation.language == language,
        Translation.is_active == True
    ).all()
    
    translation_dict = {t.key: t.value for t in translations}
    return TranslationResponse(translations=translation_dict)

@router.post("/", response_model=TranslationSchema)
def create_translation(translation: TranslationCreate, db: Session = Depends(get_db)):
    """Create a new translation"""
    # Check if translation already exists
    existing = db.query(Translation).filter(
        Translation.language == translation.language,
        Translation.key == translation.key
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation already exists for this language and key"
        )
    
    db_translation = Translation(**translation.dict())
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation

@router.post("/bulk", response_model=List[TranslationSchema])
def create_bulk_translations(bulk_data: BulkTranslationCreate, db: Session = Depends(get_db)):
    """Create multiple translations at once"""
    translations = []
    
    for translation_data in bulk_data.translations:
        # Check if translation already exists
        existing = db.query(Translation).filter(
            Translation.language == translation_data.language,
            Translation.key == translation_data.key
        ).first()
        
        if existing:
            # Update existing translation
            for field, value in translation_data.dict().items():
                setattr(existing, field, value)
            translations.append(existing)
        else:
            # Create new translation
            db_translation = Translation(**translation_data.dict())
            db.add(db_translation)
            translations.append(db_translation)
    
    db.commit()
    
    # Refresh all translations
    for translation in translations:
        db.refresh(translation)
    
    return translations

@router.put("/{translation_id}", response_model=TranslationSchema)
def update_translation(
    translation_id: int, 
    translation_update: TranslationUpdate, 
    db: Session = Depends(get_db)
):
    """Update a translation"""
    db_translation = db.query(Translation).filter(Translation.id == translation_id).first()
    
    if not db_translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation not found"
        )
    
    update_data = translation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_translation, field, value)
    
    db.commit()
    db.refresh(db_translation)
    return db_translation

@router.put("/bulk/update", response_model=List[TranslationSchema])
def update_bulk_translations(bulk_update: BulkTranslationUpdate, db: Session = Depends(get_db)):
    """Update multiple translations at once"""
    updated_translations = []
    
    for update_data in bulk_update.updates:
        translation_id = update_data.get('id')
        if not translation_id:
            continue
            
        db_translation = db.query(Translation).filter(Translation.id == translation_id).first()
        if not db_translation:
            continue
        
        # Update fields
        for field, value in update_data.items():
            if field != 'id' and hasattr(db_translation, field):
                setattr(db_translation, field, value)
        
        updated_translations.append(db_translation)
    
    db.commit()
    
    # Refresh all translations
    for translation in updated_translations:
        db.refresh(translation)
    
    return updated_translations

@router.delete("/{translation_id}")
def delete_translation(translation_id: int, db: Session = Depends(get_db)):
    """Delete a translation (soft delete by setting is_active to False)"""
    db_translation = db.query(Translation).filter(Translation.id == translation_id).first()
    
    if not db_translation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation not found"
        )
    
    db_translation.is_active = False
    db.commit()
    
    return {"message": "Translation deleted successfully"}

@router.get("/category/{category}/{language}", response_model=TranslationResponse)
def get_translations_by_category(category: str, language: str, db: Session = Depends(get_db)):
    """Get translations for a specific category and language"""
    translations = db.query(Translation).filter(
        Translation.category == category,
        Translation.language == language,
        Translation.is_active == True
    ).all()
    
    translation_dict = {t.key: t.value for t in translations}
    return TranslationResponse(translations=translation_dict) 