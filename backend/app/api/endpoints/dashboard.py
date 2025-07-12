from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from typing import List, Optional, Dict, Tuple
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
    priority: str  # "high", "medium", "low"
    expected_harvest_date: datetime
    market_demand_score: float


class DashboardData(BaseModel):
    summary: DashboardSummary
    upcoming_harvests: List[UpcomingHarvest]
    planting_suggestions: List[PlantingSuggestion]


def get_crop_growth_cycles() -> Dict[str, int]:
    """
    Define typical growth cycles for different crops (in days).
    
    This data is used to calculate when crops will be ready for harvest
    and to align planting with market opportunities.
    
    Returns:
        Dict[str, int]: Mapping of crop names to their growth cycles in days
        
    Example:
        >>> get_crop_growth_cycles()
        {'Lettuce': 45, 'Spinach': 40, 'Kale': 55, ...}
    """
    return {
        "Lettuce": 45,
        "Spinach": 40,
        "Kale": 55,
        "Arugula": 35,
        "Basil": 60,
        "Cilantro": 50,
        "Mint": 70,
        "Parsley": 75,
        "Chard": 60,
        "Mustard Greens": 45,
        "Bok Choy": 50,
        "Radish": 30,
        "Carrot": 70,
        "Beet": 60,
        "Turnip": 50,
    }


def get_seasonal_crop_preferences() -> Dict[str, List[str]]:
    """
    Define which crops are best suited for different seasons.
    
    This helps optimize planting decisions based on seasonal growing conditions
    and market preferences. Crops listed for each season are considered
    optimal for that time of year.
    
    Returns:
        Dict[str, List[str]]: Mapping of seasons to preferred crops
        
    Example:
        >>> get_seasonal_crop_preferences()
        {'spring': ['Lettuce', 'Spinach', 'Arugula', ...], ...}
    """
    return {
        "spring": ["Lettuce", "Spinach", "Arugula", "Radish", "Peas"],
        "summer": ["Basil", "Cilantro", "Mint", "Chard", "Bok Choy"],
        "fall": ["Kale", "Spinach", "Mustard Greens", "Turnip", "Carrot"],
        "winter": ["Kale", "Spinach", "Chard", "Mustard Greens"],
    }


def get_market_demand_scores() -> Dict[str, float]:
    """
    Define market demand scores for different crops (0.0 to 1.0).
    
    These scores represent the relative market demand for each crop,
    where higher scores indicate higher demand and better market opportunities.
    Scores are based on market research and customer preferences.
    
    Returns:
        Dict[str, float]: Mapping of crop names to demand scores (0.0-1.0)
        
    Example:
        >>> get_market_demand_scores()
        {'Lettuce': 0.9, 'Spinach': 0.8, 'Kale': 0.7, ...}
    """
    return {
        "Lettuce": 0.9,
        "Spinach": 0.8,
        "Kale": 0.7,
        "Arugula": 0.6,
        "Basil": 0.8,
        "Cilantro": 0.7,
        "Mint": 0.5,
        "Parsley": 0.6,
        "Chard": 0.6,
        "Mustard Greens": 0.5,
        "Bok Choy": 0.7,
        "Radish": 0.6,
        "Carrot": 0.8,
        "Beet": 0.6,
        "Turnip": 0.5,
    }


def get_current_season() -> str:
    """
    Determine current season based on date.
    
    Uses the current month to determine which season we're in,
    which affects crop recommendations and seasonal scoring.
    
    Returns:
        str: Current season ('spring', 'summer', 'fall', or 'winter')
        
    Example:
        >>> get_current_season()
        'summer'
    """
    now = datetime.now()
    month = now.month
    
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:
        return "winter"


def find_available_lines(db: Session, farm_id: Optional[int] = None) -> List[Tuple[Line, Bed]]:
    """
    Find lines that are currently available for planting.
    
    This function identifies lines that don't have any active plantings,
    making them available for new plantings. It considers both the line
    and bed status to ensure they're active and available.
    
    Args:
        db (Session): Database session for queries
        farm_id (Optional[int]): Filter by specific farm ID
        
    Returns:
        List[Tuple[Line, Bed]]: List of available (line, bed) tuples
        
    Example:
        >>> available_lines = find_available_lines(db, farm_id=1)
        >>> len(available_lines)
        5
    """
    now = datetime.now()
    
    # Get all active lines
    lines_query = (
        db.query(Line, Bed)
        .join(Bed, Line.bed_id == Bed.id)
        .filter(
            and_(
                Line.is_active == True,
                Bed.is_active == True
            )
        )
    )
    
    if farm_id:
        lines_query = lines_query.filter(Bed.farm_id == farm_id)
    
    all_lines = lines_query.all()
    available_lines = []
    
    for line, bed in all_lines:
        # Check if this line has any active plantings
        active_planting = (
            db.query(Planting)
            .filter(
                and_(
                    Planting.line_id == line.id,
                    Planting.is_active == True,
                    Planting.actual_harvest_date.is_(None)
                )
            )
            .first()
        )
        
        if not active_planting:
            available_lines.append((line, bed))
    
    return available_lines


def calculate_planting_recommendations(
    db: Session, 
    available_lines: List[Tuple[Line, Bed]], 
    weeks_ahead: int
) -> List[PlantingSuggestion]:
    """
    Calculate intelligent planting recommendations based on multiple factors.
    
    This is the main algorithm that evaluates each crop for each available line
    and provides data-driven recommendations. The algorithm considers:
    
    - Market demand (40% weight)
    - Seasonal suitability (30% weight) 
    - Market timing alignment (30% weight)
    - Historical yield performance (bonus)
    - Crop diversity (bonus)
    
    The scoring system helps farmers make optimal planting decisions that
    maximize both yield and market opportunity while managing risk.
    
    Args:
        db (Session): Database session for queries
        available_lines (List[Tuple[Line, Bed]]): Lines available for planting
        weeks_ahead (int): Number of weeks to look ahead for planning
        
    Returns:
        List[PlantingSuggestion]: Sorted list of planting recommendations
        
    Example:
        >>> recommendations = calculate_planting_recommendations(db, available_lines, 2)
        >>> len(recommendations)
        3
        >>> recommendations[0].priority
        'high'
    """
    now = datetime.now()
    growth_cycles = get_crop_growth_cycles()
    seasonal_preferences = get_seasonal_crop_preferences()
    market_demand = get_market_demand_scores()
    current_season = get_current_season()
    
    # Get upcoming selling dates
    upcoming_selling_dates = (
        db.query(SellingSchedule)
        .filter(
            and_(
                SellingSchedule.selling_date >= now,
                SellingSchedule.is_active == True
            )
        )
        .order_by(SellingSchedule.selling_date)
        .limit(3)
        .all()
    )
    
    # Get historical harvest data for yield prediction
    recent_harvests = (
        db.query(Harvest)
        .filter(Harvest.harvest_date >= now - timedelta(days=90))
        .all()
    )
    
    # Calculate average yields by crop
    crop_yields = {}
    for harvest in recent_harvests:
        crop_name = db.query(Crop).filter(Crop.id == harvest.crop_id).first()
        if crop_name:
            if crop_name.name not in crop_yields:
                crop_yields[crop_name.name] = []
            crop_yields[crop_name.name].append(harvest.harvested_quantity)
    
    # Calculate average yields
    avg_yields = {}
    for crop, yields in crop_yields.items():
        if yields:
            avg_yields[crop] = sum(yields) / len(yields)
    
    recommendations = []
    
    for line, bed in available_lines:
        best_crop = None
        best_score = 0
        best_reason = ""
        best_harvest_date = None
        
        # Evaluate each crop for this line
        for crop_name, growth_days in growth_cycles.items():
            score = 0
            reason_parts = []
            
            # Market demand score (0-1) - 40% weight
            demand_score = market_demand.get(crop_name, 0.5)
            score += demand_score * 0.4
            if demand_score > 0.7:
                reason_parts.append("High market demand")
            
            # Seasonal preference (0-1) - 30% weight
            seasonal_score = 1.0 if crop_name in seasonal_preferences.get(current_season, []) else 0.5
            score += seasonal_score * 0.3
            if seasonal_score > 0.8:
                reason_parts.append(f"Good for {current_season} season")
            
            # Growth cycle timing (0-1) - 30% weight
            # Check if harvest would align with selling dates
            planting_date = now
            harvest_date = planting_date + timedelta(days=growth_days)
            
            timing_score = 0
            for selling_date in upcoming_selling_dates:
                days_diff = abs((harvest_date - selling_date.selling_date).days)
                if days_diff <= 7:  # Within a week of selling date
                    timing_score = 1.0
                    reason_parts.append("Perfect timing for market")
                    break
                elif days_diff <= 14:  # Within two weeks
                    timing_score = 0.8
                    if "Perfect timing" not in reason_parts:
                        reason_parts.append("Good timing for market")
            
            score += timing_score * 0.3
            
            # Historical yield bonus (0-0.2)
            if crop_name in avg_yields:
                yield_bonus = min(avg_yields[crop_name] / 100, 0.2)  # Cap at 0.2
                score += yield_bonus
                if yield_bonus > 0.1:
                    reason_parts.append("Historically good yields")
            
            # Check if this crop is already heavily planted
            current_plantings = (
                db.query(Planting)
                .filter(
                    and_(
                        Planting.crop_id == db.query(Crop.id).filter(Crop.name == crop_name).scalar(),
                        Planting.is_active == True
                    )
                )
                .count()
            )
            
            # Diversity bonus (avoid over-planting same crop)
            if current_plantings < 3:
                score += 0.1
                if not reason_parts:
                    reason_parts.append("Good crop diversity")
            
            if score > best_score:
                best_score = score
                best_crop = crop_name
                best_reason = "; ".join(reason_parts) if reason_parts else "Balanced recommendation"
                best_harvest_date = harvest_date
        
        if best_crop:
            # Determine priority based on score
            if best_score >= 0.8:
                priority = "high"
            elif best_score >= 0.6:
                priority = "medium"
            else:
                priority = "low"
            
            recommendations.append(
                PlantingSuggestion(
                    bed_id=bed.id,
                    bed_name=bed.name,
                    line_id=line.id,
                    line_name=line.name,
                    available_date=now,
                    suggested_crop=best_crop,
                    reason=best_reason,
                    priority=priority,
                    expected_harvest_date=best_harvest_date,
                    market_demand_score=market_demand.get(best_crop, 0.5),
                )
            )
    
    # Sort by priority and score
    recommendations.sort(key=lambda x: (x.priority == "high", x.market_demand_score), reverse=True)
    
    return recommendations


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
        
        # Get intelligent planting suggestions
        available_lines = find_available_lines(db, farm_id)
        planting_suggestions = calculate_planting_recommendations(db, available_lines, weeks_ahead)
        
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