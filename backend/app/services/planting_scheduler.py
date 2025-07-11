from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.crop import Crop
from app.models.bed import Bed
from app.models.planting import Planting
from app.models.selling_schedule import SellingSchedule
from app.schemas.planting import PlantingSuggestion

class PlantingScheduler:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_planting_suggestions(
        self,
        farm_id: int,
        selling_schedule_id: int,
        target_date: datetime,
        frequency_days: int
    ) -> List[PlantingSuggestion]:
        """
        Generate planting suggestions based on selling schedule and farm layout
        """
        # Get selling schedule
        selling_schedule = self.db.query(SellingSchedule).filter(
            SellingSchedule.id == selling_schedule_id,
            SellingSchedule.farm_id == farm_id
        ).first()
        
        if not selling_schedule:
            raise ValueError("Selling schedule not found")
        
        # Get available beds
        beds = self.db.query(Bed).filter(
            Bed.farm_id == farm_id,
            Bed.is_active == True
        ).all()
        
        # Get available crops
        crops = self.db.query(Crop).filter(Crop.is_active == True).all()
        
        # Calculate selling dates
        selling_dates = self._calculate_selling_dates(target_date, frequency_days, 12)  # 12 months ahead
        
        # Generate suggestions for each selling date
        suggestions = []
        for selling_date in selling_dates:
            planting_suggestions = self._suggest_plantings_for_date(
                selling_date, beds, crops, farm_id
            )
            suggestions.extend(planting_suggestions)
        
        return suggestions
    
    def _calculate_selling_dates(
        self, 
        start_date: datetime, 
        frequency_days: int, 
        months_ahead: int
    ) -> List[datetime]:
        """Calculate all selling dates for the next X months"""
        dates = []
        current_date = start_date
        
        end_date = start_date + timedelta(days=months_ahead * 30)
        
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=frequency_days)
        
        return dates
    
    def _suggest_plantings_for_date(
        self,
        selling_date: datetime,
        beds: List[Bed],
        crops: List[Crop],
        farm_id: int
    ) -> List[PlantingSuggestion]:
        """Suggest what to plant for a specific selling date"""
        suggestions = []
        
        # Calculate planting date (selling date - growing time)
        for crop in crops:
            planting_date = selling_date - timedelta(days=crop.growing_time_days)
            
            # Check if planting date is in the future
            if planting_date > datetime.now():
                # Check if crop is suitable for the planting season
                if self._is_crop_suitable_for_date(crop, planting_date):
                    # Find available beds
                    available_beds = self._find_available_beds(beds, planting_date, farm_id)
                    
                    if available_beds:
                        suggestion = PlantingSuggestion(
                            crop_id=crop.id,
                            crop_name=crop.name,
                            bed_id=available_beds[0].id,
                            bed_name=available_beds[0].name,
                            planting_date=planting_date,
                            expected_harvest_date=selling_date,
                            suggested_quantity=self._calculate_planting_quantity(
                                crop, available_beds[0]
                            ),
                            priority=self._calculate_priority(crop, selling_date)
                        )
                        suggestions.append(suggestion)
        
        # Sort by priority
        suggestions.sort(key=lambda x: x.priority, reverse=True)
        return suggestions
    
    def _is_crop_suitable_for_date(self, crop: Crop, planting_date: datetime) -> bool:
        """Check if crop is suitable for planting on the given date"""
        if not crop.best_planting_seasons:
            return True
        
        planting_month = planting_date.month
        return planting_month in crop.best_planting_seasons
    
    def _find_available_beds(
        self, 
        beds: List[Bed], 
        planting_date: datetime, 
        farm_id: int
    ) -> List[Bed]:
        """Find beds that are available for planting on the given date"""
        available_beds = []
        
        for bed in beds:
            # Check if bed has active plantings that would conflict
            conflicting_plantings = self.db.query(Planting).filter(
                Planting.bed_id == bed.id,
                Planting.is_active == True,
                Planting.planted_date <= planting_date,
                Planting.expected_harvest_date >= planting_date
            ).first()
            
            if not conflicting_plantings:
                available_beds.append(bed)
        
        return available_beds
    
    def _calculate_planting_quantity(self, crop: Crop, bed: Bed) -> int:
        """Calculate how many plants to suggest based on bed area and crop spacing"""
        if not crop.spacing_cm or not crop.row_spacing_cm:
            return 1  # Default to 1 if spacing not defined
        
        # Calculate plants per square meter
        spacing_sqm = (crop.spacing_cm / 100) * (crop.row_spacing_cm / 100)
        plants_per_sqm = 1 / spacing_sqm
        
        # Calculate total plants for the bed
        total_plants = int(bed.area * plants_per_sqm)
        
        return max(1, total_plants)
    
    def _calculate_priority(self, crop: Crop, selling_date: datetime) -> float:
        """Calculate priority score for crop suggestion"""
        priority = 0.0
        
        # Market price factor
        if crop.market_price_per_kg:
            priority += crop.market_price_per_kg * 0.3
        
        # Yield factor
        if crop.expected_yield_per_sqm:
            priority += crop.expected_yield_per_sqm * 0.2
        
        # Seasonal factor (higher priority for seasonal crops)
        if crop.best_planting_seasons:
            current_month = selling_date.month
            if current_month in crop.best_planting_seasons:
                priority += 0.5
        
        # Storage life factor (longer storage = higher priority)
        if crop.storage_life_days:
            priority += min(crop.storage_life_days / 30, 1.0) * 0.1
        
        return priority 