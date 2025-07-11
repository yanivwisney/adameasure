from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.selling_schedule import SellingSchedule
from app.schemas.selling_schedule import (
    SellingScheduleCreate, 
    SellingScheduleUpdate, 
    SellingSchedule as SellingScheduleSchema
)

router = APIRouter()

@router.post("/", response_model=SellingScheduleSchema, status_code=status.HTTP_201_CREATED)
def create_selling_schedule(schedule: SellingScheduleCreate, db: Session = Depends(get_db)):
    """Create a new selling schedule"""
    db_schedule = SellingSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/", response_model=List[SellingScheduleSchema])
def get_selling_schedules(
    farm_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all selling schedules with optional filters"""
    query = db.query(SellingSchedule)
    
    if farm_id:
        query = query.filter(SellingSchedule.farm_id == farm_id)
    if is_active is not None:
        query = query.filter(SellingSchedule.is_active == is_active)
    
    schedules = query.offset(skip).limit(limit).all()
    return schedules

@router.get("/{schedule_id}", response_model=SellingScheduleSchema)
def get_selling_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Get a specific selling schedule by ID"""
    schedule = db.query(SellingSchedule).filter(SellingSchedule.id == schedule_id).first()
    if schedule is None:
        raise HTTPException(status_code=404, detail="Selling schedule not found")
    return schedule

@router.put("/{schedule_id}", response_model=SellingScheduleSchema)
def update_selling_schedule(schedule_id: int, schedule: SellingScheduleUpdate, db: Session = Depends(get_db)):
    """Update a selling schedule"""
    db_schedule = db.query(SellingSchedule).filter(SellingSchedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Selling schedule not found")
    
    update_data = schedule.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_schedule, field, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_selling_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """Delete a selling schedule"""
    db_schedule = db.query(SellingSchedule).filter(SellingSchedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Selling schedule not found")
    
    db.delete(db_schedule)
    db.commit()
    return None 