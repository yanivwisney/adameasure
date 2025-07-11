from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.farm import Farm
from app.schemas.farm import FarmCreate, FarmUpdate, Farm as FarmSchema, FarmWithBeds

router = APIRouter()

@router.post("/", response_model=FarmSchema, status_code=status.HTTP_201_CREATED)
def create_farm(farm: FarmCreate, db: Session = Depends(get_db)):
    """Create a new farm"""
    db_farm = Farm(**farm.dict())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.get("/", response_model=List[FarmSchema])
def get_farms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all farms"""
    farms = db.query(Farm).offset(skip).limit(limit).all()
    return farms

@router.get("/{farm_id}", response_model=FarmWithBeds)
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    """Get a specific farm by ID"""
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@router.put("/{farm_id}", response_model=FarmSchema)
def update_farm(farm_id: int, farm: FarmUpdate, db: Session = Depends(get_db)):
    """Update a farm"""
    db_farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if db_farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    
    update_data = farm.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_farm, field, value)
    
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    """Delete a farm"""
    db_farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if db_farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    
    db.delete(db_farm)
    db.commit()
    return None 