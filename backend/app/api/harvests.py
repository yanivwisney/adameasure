from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db
from ..models.harvest import Harvest
from ..models.planting import Planting
from ..models.crop import Crop
from ..models.bed import Bed
from ..models.line import Line
from ..schemas.harvest import HarvestCreate, HarvestUpdate, HarvestResponse, HarvestSummary

router = APIRouter(prefix="/harvests", tags=["harvests"])

@router.post("/", response_model=HarvestResponse)
def create_harvest(harvest: HarvestCreate, db: Session = Depends(get_db)):
    """Record a new harvest with automatic timing and yield analysis"""
    
    # Get the planting to calculate expected dates and yields
    planting = db.query(Planting).filter(Planting.id == harvest.planting_id).first()
    if not planting:
        raise HTTPException(status_code=404, detail="Planting not found")
    
    # Get crop data for yield calculations
    crop = db.query(Crop).filter(Crop.id == harvest.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Calculate timing analysis
    days_early_late = None
    expected_harvest_date = None
    
    if planting.expected_harvest_date:
        expected_harvest_date = planting.expected_harvest_date
        days_early_late = (harvest.harvest_date - planting.expected_harvest_date).days
    
    # Calculate yield analysis
    expected_yield = None
    yield_percentage = None
    
    if crop.expected_yield_per_plant and planting.quantity:
        expected_yield = crop.expected_yield_per_plant * planting.quantity
        if expected_yield > 0:
            yield_percentage = (harvest.harvested_quantity / expected_yield) * 100
    
    # Create harvest record
    db_harvest = Harvest(
        **harvest.dict(),
        days_early_late=days_early_late,
        expected_harvest_date=expected_harvest_date,
        expected_yield=expected_yield,
        yield_percentage=yield_percentage
    )
    
    db.add(db_harvest)
    db.commit()
    db.refresh(db_harvest)
    
    # Update planting with harvest data
    planting.actual_harvest_date = harvest.harvest_date
    planting.harvested_quantity = harvest.harvested_quantity
    db.commit()
    
    return db_harvest

@router.get("/", response_model=List[HarvestSummary])
def get_harvests(
    farm_id: Optional[int] = None,
    bed_id: Optional[int] = None,
    crop_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get harvests with optional filtering"""
    query = db.query(Harvest).join(Crop).join(Bed).join(Line)
    
    if farm_id:
        query = query.filter(Harvest.farm_id == farm_id)
    if bed_id:
        query = query.filter(Harvest.bed_id == bed_id)
    if crop_id:
        query = query.filter(Harvest.crop_id == crop_id)
    if start_date:
        query = query.filter(Harvest.harvest_date >= start_date)
    if end_date:
        query = query.filter(Harvest.harvest_date <= end_date)
    
    harvests = query.order_by(Harvest.harvest_date.desc()).all()
    
    # Convert to summary format
    summaries = []
    for harvest in harvests:
        summary = HarvestSummary(
            id=harvest.id,
            crop_name=harvest.crop.name,
            bed_name=harvest.bed.name,
            line_name=harvest.line.name,
            harvest_date=harvest.harvest_date,
            harvested_quantity=harvest.harvested_quantity,
            quality_rating=harvest.quality_rating,
            days_early_late=harvest.days_early_late,
            yield_percentage=harvest.yield_percentage,
            is_complete=harvest.is_complete
        )
        summaries.append(summary)
    
    return summaries

@router.get("/{harvest_id}", response_model=HarvestResponse)
def get_harvest(harvest_id: int, db: Session = Depends(get_db)):
    """Get a specific harvest by ID"""
    harvest = db.query(Harvest).filter(Harvest.id == harvest_id).first()
    if not harvest:
        raise HTTPException(status_code=404, detail="Harvest not found")
    return harvest

@router.put("/{harvest_id}", response_model=HarvestResponse)
def update_harvest(harvest_id: int, harvest_update: HarvestUpdate, db: Session = Depends(get_db)):
    """Update a harvest record"""
    db_harvest = db.query(Harvest).filter(Harvest.id == harvest_id).first()
    if not db_harvest:
        raise HTTPException(status_code=404, detail="Harvest not found")
    
    # Update fields
    update_data = harvest_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_harvest, field, value)
    
    # Recalculate timing and yield if harvest date or quantity changed
    if harvest_update.harvest_date or harvest_update.harvested_quantity:
        planting = db.query(Planting).filter(Planting.id == db_harvest.planting_id).first()
        crop = db.query(Crop).filter(Crop.id == db_harvest.crop_id).first()
        
        if planting and planting.expected_harvest_date:
            db_harvest.expected_harvest_date = planting.expected_harvest_date
            db_harvest.days_early_late = (db_harvest.harvest_date - planting.expected_harvest_date).days
        
        if crop and crop.expected_yield_per_plant and planting.quantity:
            expected_yield = crop.expected_yield_per_plant * planting.quantity
            db_harvest.expected_yield = expected_yield
            if expected_yield > 0:
                db_harvest.yield_percentage = (db_harvest.harvested_quantity / expected_yield) * 100
    
    db.commit()
    db.refresh(db_harvest)
    return db_harvest

@router.delete("/{harvest_id}")
def delete_harvest(harvest_id: int, db: Session = Depends(get_db)):
    """Delete a harvest record"""
    harvest = db.query(Harvest).filter(Harvest.id == harvest_id).first()
    if not harvest:
        raise HTTPException(status_code=404, detail="Harvest not found")
    
    db.delete(harvest)
    db.commit()
    return {"message": "Harvest deleted successfully"}

@router.get("/analytics/summary")
def get_harvest_analytics(
    farm_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get harvest analytics and performance metrics"""
    query = db.query(Harvest)
    
    if farm_id:
        query = query.filter(Harvest.farm_id == farm_id)
    if start_date:
        query = query.filter(Harvest.harvest_date >= start_date)
    if end_date:
        query = query.filter(Harvest.harvest_date <= end_date)
    
    harvests = query.all()
    
    if not harvests:
        return {
            "total_harvests": 0,
            "total_yield": 0,
            "average_quality": 0,
            "timing_performance": {},
            "yield_performance": {}
        }
    
    # Calculate analytics
    total_harvests = len(harvests)
    total_yield = sum(h.harvested_quantity for h in harvests)
    quality_ratings = [h.quality_rating for h in harvests if h.quality_rating]
    average_quality = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0
    
    # Timing performance
    early_harvests = [h for h in harvests if h.days_early_late and h.days_early_late > 0]
    late_harvests = [h for h in harvests if h.days_early_late and h.days_early_late < 0]
    on_time_harvests = [h for h in harvests if h.days_early_late == 0]
    
    # Yield performance
    high_yield = [h for h in harvests if h.yield_percentage and h.yield_percentage > 100]
    low_yield = [h for h in harvests if h.yield_percentage and h.yield_percentage < 80]
    expected_yield = [h for h in harvests if h.yield_percentage and 80 <= h.yield_percentage <= 100]
    
    return {
        "total_harvests": total_harvests,
        "total_yield": total_yield,
        "average_quality": round(average_quality, 2),
        "timing_performance": {
            "early_harvests": len(early_harvests),
            "late_harvests": len(late_harvests),
            "on_time_harvests": len(on_time_harvests),
            "early_percentage": round(len(early_harvests) / total_harvests * 100, 1) if total_harvests > 0 else 0,
            "late_percentage": round(len(late_harvests) / total_harvests * 100, 1) if total_harvests > 0 else 0
        },
        "yield_performance": {
            "high_yield": len(high_yield),
            "low_yield": len(low_yield),
            "expected_yield": len(expected_yield),
            "high_yield_percentage": round(len(high_yield) / total_harvests * 100, 1) if total_harvests > 0 else 0,
            "low_yield_percentage": round(len(low_yield) / total_harvests * 100, 1) if total_harvests > 0 else 0
        }
    } 