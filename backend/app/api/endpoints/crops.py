from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.crop import Crop
from app.schemas.crop import CropCreate, CropUpdate, Crop as CropSchema

router = APIRouter()


@router.post("/", response_model=CropSchema, status_code=status.HTTP_201_CREATED)
def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    """Create a new crop"""
    db_crop = Crop(**crop.dict())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop


@router.get("/", response_model=List[CropSchema])
def get_crops(
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all crops with optional filters"""
    query = db.query(Crop)

    if category:
        query = query.filter(Crop.category == category)
    if is_active is not None:
        query = query.filter(Crop.is_active == is_active)

    crops = query.offset(skip).limit(limit).all()
    return crops


@router.get("/{crop_id}", response_model=CropSchema)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """Get a specific crop by ID"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if crop is None:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


@router.put("/{crop_id}", response_model=CropSchema)
def update_crop(crop_id: int, crop: CropUpdate, db: Session = Depends(get_db)):
    """Update a crop"""
    db_crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if db_crop is None:
        raise HTTPException(status_code=404, detail="Crop not found")

    update_data = crop.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_crop, field, value)

    db.commit()
    db.refresh(db_crop)
    return db_crop


@router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """Delete a crop"""
    db_crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if db_crop is None:
        raise HTTPException(status_code=404, detail="Crop not found")

    db.delete(db_crop)
    db.commit()
    return None


@router.get("/categories/list")
def get_crop_categories(db: Session = Depends(get_db)):
    """Get all unique crop categories"""
    categories = db.query(Crop.category).distinct().all()
    return [category[0] for category in categories]
