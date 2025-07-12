from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.planting import Planting
from app.schemas.planting import (
    PlantingCreate,
    PlantingUpdate,
    Planting as PlantingSchema,
    PlantingSuggestion,
    PlantingScheduleRequest,
)
from app.services.planting_scheduler import PlantingScheduler
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=PlantingSchema, status_code=status.HTTP_201_CREATED)
def create_planting(planting: PlantingCreate, db: Session = Depends(get_db)):
    """Create a new planting record"""
    db_planting = Planting(**planting.dict())
    db.add(db_planting)
    db.commit()
    db.refresh(db_planting)
    return db_planting


@router.get("/", response_model=List[PlantingSchema])
def get_plantings(
    farm_id: Optional[int] = None,
    bed_id: Optional[int] = None,
    crop_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all plantings with optional filters"""
    query = db.query(Planting)

    if farm_id:
        query = query.filter(Planting.farm_id == farm_id)
    if bed_id:
        query = query.filter(Planting.bed_id == bed_id)
    if crop_id:
        query = query.filter(Planting.crop_id == crop_id)

    plantings = query.offset(skip).limit(limit).all()
    return plantings


@router.get("/{planting_id}", response_model=PlantingSchema)
def get_planting(planting_id: int, db: Session = Depends(get_db)):
    """Get a specific planting by ID"""
    planting = db.query(Planting).filter(Planting.id == planting_id).first()
    if planting is None:
        raise HTTPException(status_code=404, detail="Planting not found")
    return planting


@router.put("/{planting_id}", response_model=PlantingSchema)
def update_planting(
    planting_id: int, planting: PlantingUpdate, db: Session = Depends(get_db)
):
    """Update a planting record"""
    db_planting = db.query(Planting).filter(Planting.id == planting_id).first()
    if db_planting is None:
        raise HTTPException(status_code=404, detail="Planting not found")

    update_data = planting.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_planting, field, value)

    db.commit()
    db.refresh(db_planting)
    return db_planting


@router.delete("/{planting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_planting(planting_id: int, db: Session = Depends(get_db)):
    """Delete a planting record"""
    db_planting = db.query(Planting).filter(Planting.id == planting_id).first()
    if db_planting is None:
        raise HTTPException(status_code=404, detail="Planting not found")

    db.delete(db_planting)
    db.commit()
    return None


@router.post("/suggestions", response_model=List[PlantingSuggestion])
def get_planting_suggestions(
    request: PlantingScheduleRequest, db: Session = Depends(get_db)
):
    """Get planting suggestions based on selling schedule"""
    try:
        scheduler = PlantingScheduler(db)
        suggestions = scheduler.generate_planting_suggestions(
            farm_id=request.farm_id,
            selling_schedule_id=request.selling_schedule_id,
            target_date=request.target_date,
            frequency_days=request.frequency_days,
        )
        return suggestions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating suggestions: {str(e)}"
        )


@router.post("/{planting_id}/harvest")
def record_harvest(
    planting_id: int,
    harvested_quantity: float,
    harvest_notes: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Record harvest for a planting"""
    db_planting = db.query(Planting).filter(Planting.id == planting_id).first()
    if db_planting is None:
        raise HTTPException(status_code=404, detail="Planting not found")

    db_planting.actual_harvest_date = datetime.now()
    db_planting.harvested_quantity = harvested_quantity
    db_planting.harvest_notes = harvest_notes
    db_planting.is_active = False

    db.commit()
    db.refresh(db_planting)
    return {"message": "Harvest recorded successfully"}
