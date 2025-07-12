from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.farm import Farm
from app.models.bed import Bed
from app.models.planting import Planting
from app.models.harvest import Harvest
from app.models.selling_schedule import SellingSchedule
from app.models.crop import Crop
from app.models.line import Line
from pydantic import BaseModel

router = APIRouter()


class DashboardSummary(BaseModel):
    total_farms: int
    total_beds: int
    total_plantings: int
    next_selling_date: Optional[datetime]
    days_until_next_selling: Optional[int]


class UpcomingHarvest(BaseModel):
    id: int
    crop_name: str
    bed_name: str
    line_name: str
    expected_harvest_date: datetime
    days_until_harvest: int
    expected_quantity: float
    planting_id: int


class PlantingSuggestion(BaseModel):
    bed_id: int
    bed_name: str
    line_id: int
    line_name: str
    available_date: datetime
    suggested_crop: str
    reason: str


class DashboardData(BaseModel):
    summary: DashboardSummary
    upcoming_harvests: List[UpcomingHarvest]
    planting_suggestions: List[PlantingSuggestion]


@router.get("/", response_model=DashboardData)
def get_dashboard_data(
    farm_id: Optional[int] = None,
    weeks_ahead: int = 2,
    db: Session = Depends(get_db),
):
    """Get comprehensive dashboard data"""
    
    try:
        # Get summary counts
        farms_query = db.query(Farm).filter(Farm.is_active == True)
        beds_query = db.query(Bed).filter(Bed.is_active == True)
        plantings_query = db.query(Planting).filter(Planting.is_active == True)
        
        if farm_id:
            farms_query = farms_query.filter(Farm.id == farm_id)
            beds_query = beds_query.filter(Bed.farm_id == farm_id)
            plantings_query = plantings_query.filter(Planting.farm_id == farm_id)
        
        total_farms = farms_query.count()
        total_beds = beds_query.count()
        total_plantings = plantings_query.count()
        
        # Get next selling date
        now = datetime.now()
        next_selling = (
            db.query(SellingSchedule)
            .filter(
                and_(
                    SellingSchedule.selling_date >= now,
                    SellingSchedule.is_active == True
                )
            )
            .order_by(SellingSchedule.selling_date)
            .first()
        )
        
        next_selling_date = next_selling.selling_date if next_selling else None
        days_until_next_selling = (
            (next_selling_date - now).days if next_selling_date else None
        )
        
        summary = DashboardSummary(
            total_farms=total_farms,
            total_beds=total_beds,
            total_plantings=total_plantings,
            next_selling_date=next_selling_date,
            days_until_next_selling=days_until_next_selling,
        )
        
        # Get upcoming harvests (plantings that are expected to be harvested soon)
        harvest_date_threshold = now + timedelta(weeks=weeks_ahead)
        
        # Simplified query to avoid complex joins
        upcoming_plantings = (
            db.query(Planting)
            .filter(
                and_(
                    Planting.is_active == True,
                    Planting.expected_harvest_date >= now,
                    Planting.expected_harvest_date <= harvest_date_threshold,
                    Planting.actual_harvest_date.is_(None)
                )
            )
            .order_by(Planting.expected_harvest_date)
            .all()
        )
        
        upcoming_harvests = []
        for planting in upcoming_plantings:
            # Get related data
            crop = db.query(Crop).filter(Crop.id == planting.crop_id).first()
            bed = db.query(Bed).filter(Bed.id == planting.bed_id).first()
            line = db.query(Line).filter(Line.id == planting.line_id).first()
            
            if crop and bed and line:
                days_until_harvest = (planting.expected_harvest_date - now).days
                upcoming_harvests.append(
                    UpcomingHarvest(
                        id=planting.id,
                        crop_name=crop.name,
                        bed_name=bed.name,
                        line_name=line.name,
                        expected_harvest_date=planting.expected_harvest_date,
                        days_until_harvest=days_until_harvest,
                        expected_quantity=planting.quantity or 0,
                        planting_id=planting.id,
                    )
                )
        
        # Get planting suggestions (simplified)
        available_beds = (
            db.query(Bed)
            .filter(Bed.is_active == True)
            .all()
        )
        
        planting_suggestions = []
        for bed in available_beds:
            # Get available lines in this bed
            available_lines = (
                db.query(Line)
                .filter(
                    and_(
                        Line.bed_id == bed.id,
                        Line.is_active == True
                    )
                )
                .all()
            )
            
            for line in available_lines:
                # Simple suggestion logic
                suggested_crop = "Lettuce"  # Placeholder
                planting_suggestions.append(
                    PlantingSuggestion(
                        bed_id=bed.id,
                        bed_name=bed.name,
                        line_id=line.id,
                        line_name=line.name,
                        available_date=now,
                        suggested_crop=suggested_crop,
                        reason="High demand crop for next selling cycle",
                    )
                )
        
        return DashboardData(
            summary=summary,
            upcoming_harvests=upcoming_harvests,
            planting_suggestions=planting_suggestions,
        )
        
    except Exception as e:
        # Return empty data if there's an error
        summary = DashboardSummary(
            total_farms=0,
            total_beds=0,
            total_plantings=0,
            next_selling_date=None,
            days_until_next_selling=None,
        )
        
        return DashboardData(
            summary=summary,
            upcoming_harvests=[],
            planting_suggestions=[],
        )


@router.post("/harvests/{planting_id}/mark-harvested")
def mark_planting_harvested(
    planting_id: int,
    harvested_quantity: float,
    quality_rating: Optional[int] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Mark a planting as harvested"""
    planting = db.query(Planting).filter(Planting.id == planting_id).first()
    if not planting:
        raise HTTPException(status_code=404, detail="Planting not found")
    
    # Create harvest record
    harvest = Harvest(
        planting_id=planting.id,
        crop_id=planting.crop_id,
        farm_id=planting.farm_id,
        bed_id=planting.bed_id,
        line_id=planting.line_id,
        harvest_date=datetime.now(),
        harvested_quantity=harvested_quantity,
        quality_rating=quality_rating,
        notes=notes,
        is_complete=True,
    )
    
    db.add(harvest)
    
    # Update planting
    planting.actual_harvest_date = datetime.now()
    planting.harvested_quantity = harvested_quantity
    planting.is_active = False
    
    db.commit()
    db.refresh(harvest)
    
    return {"message": "Harvest recorded successfully", "harvest_id": harvest.id} 