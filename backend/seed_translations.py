#!/usr/bin/env python3
"""
Seed the database with initial translations
"""

import sys
import os
import logging
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.translation import Translation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_translations(translations_data=None):
    """
    Seed translations into the database.

    Args:
        translations_data (list): List of dictionaries with translation data.
                                 Each dict should have: language, key, value, category (optional)
    """
    if translations_data is None:
        translations_data = get_default_translations()

    db = SessionLocal()
    try:
        # Clear existing translations
        db.query(Translation).delete()
        db.commit()

        # Insert new translations
        for trans_data in translations_data:
            translation = Translation(**trans_data)
            db.add(translation)

        db.commit()
        logger.info(f"✅ Translations seeded successfully!")
        logger.info(f"📝 Added {len(translations_data)} translations")

    except Exception as e:
        logger.error(f"❌ Error seeding translations: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_default_translations():
    """Get the default translations data."""
    return [
        # Farm terms - English
        {
            "language": "en",
            "key": "farm.harvest",
            "value": "Harvest",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.planting",
            "value": "Planting",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.growing",
            "value": "Growing",
            "category": "farm_terms",
        },
        {"language": "en", "key": "farm.bed", "value": "Bed", "category": "farm_terms"},
        {
            "language": "en",
            "key": "farm.field",
            "value": "Field",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.greenhouse",
            "value": "Greenhouse",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.irrigation",
            "value": "Irrigation",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.fertilizer",
            "value": "Fertilizer",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.pesticide",
            "value": "Pesticide",
            "category": "farm_terms",
        },
        {
            "language": "en",
            "key": "farm.organic",
            "value": "Organic",
            "category": "farm_terms",
        },
        # Farm terms - Hebrew
        {
            "language": "he",
            "key": "farm.harvest",
            "value": "קטיף",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.planting",
            "value": "זריעה",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.growing",
            "value": "גידול",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.bed",
            "value": "ערוגה",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.field",
            "value": "שדה",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.greenhouse",
            "value": "חממה",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.irrigation",
            "value": "השקיה",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.fertilizer",
            "value": "דשן",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.pesticide",
            "value": "חומר הדברה",
            "category": "farm_terms",
        },
        {
            "language": "he",
            "key": "farm.organic",
            "value": "אורגני",
            "category": "farm_terms",
        },
        # UI terms - English
        {"language": "en", "key": "ui.add", "value": "Add", "category": "ui"},
        {"language": "en", "key": "ui.edit", "value": "Edit", "category": "ui"},
        {"language": "en", "key": "ui.delete", "value": "Delete", "category": "ui"},
        {"language": "en", "key": "ui.save", "value": "Save", "category": "ui"},
        {"language": "en", "key": "ui.cancel", "value": "Cancel", "category": "ui"},
        {"language": "en", "key": "ui.back", "value": "Back", "category": "ui"},
        {"language": "en", "key": "ui.next", "value": "Next", "category": "ui"},
        {"language": "en", "key": "ui.previous", "value": "Previous", "category": "ui"},
        {"language": "en", "key": "ui.search", "value": "Search", "category": "ui"},
        {"language": "en", "key": "ui.filter", "value": "Filter", "category": "ui"},
        # UI terms - Hebrew
        {"language": "he", "key": "ui.add", "value": "הוסף", "category": "ui"},
        {"language": "he", "key": "ui.edit", "value": "ערוך", "category": "ui"},
        {"language": "he", "key": "ui.delete", "value": "מחק", "category": "ui"},
        {"language": "he", "key": "ui.save", "value": "שמור", "category": "ui"},
        {"language": "he", "key": "ui.cancel", "value": "ביטול", "category": "ui"},
        {"language": "he", "key": "ui.back", "value": "חזור", "category": "ui"},
        {"language": "he", "key": "ui.next", "value": "הבא", "category": "ui"},
        {"language": "he", "key": "ui.previous", "value": "הקודם", "category": "ui"},
        {"language": "he", "key": "ui.search", "value": "חיפוש", "category": "ui"},
        {"language": "he", "key": "ui.filter", "value": "סינון", "category": "ui"},
        # Harvests - English
        {
            "language": "en",
            "key": "harvests.title",
            "value": "Harvests",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.recordHarvest",
            "value": "Record Harvest",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.recordNewHarvest",
            "value": "Record New Harvest",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.selectPlanting",
            "value": "Select Planting",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.harvestDate",
            "value": "Harvest Date",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.quantity",
            "value": "Quantity",
            "category": None,
        },
        {"language": "en", "key": "harvests.unit", "value": "Unit", "category": None},
        {
            "language": "en",
            "key": "harvests.quality",
            "value": "Quality",
            "category": None,
        },
        {"language": "en", "key": "harvests.notes", "value": "Notes", "category": None},
        {
            "language": "en",
            "key": "harvests.expectedDate",
            "value": "Expected Date",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.actualDate",
            "value": "Actual Date",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.expectedYield",
            "value": "Expected Yield",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.actualYield",
            "value": "Actual Yield",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.yieldComparison",
            "value": "Yield Comparison",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.timingAnalysis",
            "value": "Timing Analysis",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.noExpectedDate",
            "value": "No Expected Date",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.early",
            "value": "{days} days early",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.late",
            "value": "{days} days late",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.onTime",
            "value": "On Time",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.noExpectedYield",
            "value": "No Expected Yield",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.highYield",
            "value": "{percentage}% of expected (high)",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.lowYield",
            "value": "{percentage}% of expected (low)",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.expectedYield",
            "value": "{percentage}% of expected",
            "category": None,
        },
        {
            "language": "en",
            "key": "harvests.cancel",
            "value": "Cancel",
            "category": None,
        },
        # Harvests - Hebrew
        {
            "language": "he",
            "key": "harvests.title",
            "value": "קצירים",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.recordHarvest",
            "value": "הוסף קציר",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.recordNewHarvest",
            "value": "הוסף קציר חדש",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.selectPlanting",
            "value": "בחר זריעה",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.harvestDate",
            "value": "תאריך קציר",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.quantity",
            "value": "כמות",
            "category": None,
        },
        {"language": "he", "key": "harvests.unit", "value": "יחידה", "category": None},
        {
            "language": "he",
            "key": "harvests.quality",
            "value": "איכות",
            "category": None,
        },
        {"language": "he", "key": "harvests.notes", "value": "הערות", "category": None},
        {
            "language": "he",
            "key": "harvests.expectedDate",
            "value": "תאריך צפוי",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.actualDate",
            "value": "תאריך בפועל",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.expectedYield",
            "value": "תפוקה צפויה",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.actualYield",
            "value": "תפוקה בפועל",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.yieldComparison",
            "value": "השוואת תפוקה",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.timingAnalysis",
            "value": "ניתוח זמנים",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.noExpectedDate",
            "value": "אין תאריך צפוי",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.early",
            "value": "{days} ימים מוקדם",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.late",
            "value": "{days} ימים מאוחר",
            "category": None,
        },
        {"language": "he", "key": "harvests.onTime", "value": "בזמן", "category": None},
        {
            "language": "he",
            "key": "harvests.noExpectedYield",
            "value": "אין תפוקה צפויה",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.highYield",
            "value": "{percentage}% מהצפוי (גבוה)",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.lowYield",
            "value": "{percentage}% מהצפוי (נמוך)",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.expectedYield",
            "value": "{percentage}% מהצפוי",
            "category": None,
        },
        {
            "language": "he",
            "key": "harvests.cancel",
            "value": "ביטול",
            "category": None,
        },
        # Navigation - English
        {
            "language": "en",
            "key": "nav.harvests",
            "value": "Harvests",
            "category": "navigation",
        },
        # Navigation - Hebrew
        {
            "language": "he",
            "key": "nav.harvests",
            "value": "קצירים",
            "category": "navigation",
        },
        # Harvests Table - English
        {
            "language": "en",
            "key": "harvests.recentHarvests",
            "value": "Recent Harvests",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.crop",
            "value": "Crop",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.location",
            "value": "Location",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.date",
            "value": "Date",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.quantity",
            "value": "Quantity",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.timing",
            "value": "Timing",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.yield",
            "value": "Yield",
            "category": "harvests",
        },
        {
            "language": "en",
            "key": "harvests.quality",
            "value": "Quality",
            "category": "harvests",
        },
        # Harvests Table - Hebrew
        {
            "language": "he",
            "key": "harvests.recentHarvests",
            "value": "קצירים אחרונים",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.crop",
            "value": "גידול",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.location",
            "value": "מיקום",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.date",
            "value": "תאריך",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.quantity",
            "value": "כמות",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.timing",
            "value": "תזמון",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.yield",
            "value": "יבול",
            "category": "harvests",
        },
        {
            "language": "he",
            "key": "harvests.quality",
            "value": "איכות",
            "category": "harvests",
        },
        # Dashboard - English
        {"language": "en", "key": "dashboard.next_selling", "value": "Next Selling", "category": "dashboard"},
        {"language": "en", "key": "dashboard.planting_suggestions", "value": "Planting Suggestions", "category": "dashboard"},
        {"language": "en", "key": "dashboard.weeks_ahead", "value": "Weeks ahead", "category": "dashboard"},
        {"language": "en", "key": "dashboard.available", "value": "Available", "category": "dashboard"},
        {"language": "en", "key": "dashboard.suggested", "value": "Suggested", "category": "dashboard"},
        {"language": "en", "key": "dashboard.no_upcoming_harvests", "value": "No upcoming harvests", "category": "dashboard"},
        {"language": "en", "key": "dashboard.no_planting_suggestions", "value": "No planting suggestions", "category": "dashboard"},
        {"language": "en", "key": "dashboard.ready_in_days", "value": "Ready in {days} days", "category": "dashboard"},
        {"language": "en", "key": "dashboard.upcoming_count", "value": "{count} upcoming", "category": "dashboard"},
        {"language": "en", "key": "dashboard.available_count", "value": "{count} available", "category": "dashboard"},
        {"language": "en", "key": "dashboard.no_upcoming_sales", "value": "No upcoming sales", "category": "dashboard"},
        {"language": "en", "key": "dashboard.today", "value": "Today!", "category": "dashboard"},
        {"language": "en", "key": "dashboard.tomorrow", "value": "Tomorrow", "category": "dashboard"},
        {"language": "en", "key": "dashboard.days", "value": "{days} days", "category": "dashboard"},
        {"language": "en", "key": "dashboard.mark_harvested", "value": "Mark as harvested", "category": "dashboard"},
        {"language": "en", "key": "dashboard.plant_suggestion", "value": "Plant suggestion", "category": "dashboard"},
        {"language": "en", "key": "dashboard.harvest", "value": "Harvest", "category": "dashboard"},
        {"language": "en", "key": "dashboard.plant", "value": "Plant", "category": "dashboard"},
        {"language": "en", "key": "dashboard.high_demand_reason", "value": "High demand crop for next selling cycle", "category": "dashboard"},
        
        # Dashboard - Hebrew
        {"language": "he", "key": "dashboard.next_selling", "value": "מכירה הבאה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.planting_suggestions", "value": "הצעות נטיעה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.weeks_ahead", "value": "שבועות קדימה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.available", "value": "זמין", "category": "dashboard"},
        {"language": "he", "key": "dashboard.suggested", "value": "מוצע", "category": "dashboard"},
        {"language": "he", "key": "dashboard.no_upcoming_harvests", "value": "אין קצירים קרובים", "category": "dashboard"},
        {"language": "he", "key": "dashboard.no_planting_suggestions", "value": "אין הצעות נטיעה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.ready_in_days", "value": "מוכן בעוד {days} ימים", "category": "dashboard"},
        {"language": "he", "key": "dashboard.upcoming_count", "value": "{count} קרובים", "category": "dashboard"},
        {"language": "he", "key": "dashboard.available_count", "value": "{count} זמינים", "category": "dashboard"},
        {"language": "he", "key": "dashboard.no_upcoming_sales", "value": "אין מכירות קרובות", "category": "dashboard"},
        {"language": "he", "key": "dashboard.today", "value": "היום!", "category": "dashboard"},
        {"language": "he", "key": "dashboard.tomorrow", "value": "מחר", "category": "dashboard"},
        {"language": "he", "key": "dashboard.days", "value": "{days} ימים", "category": "dashboard"},
        {"language": "he", "key": "dashboard.mark_harvested", "value": "סמן כנקצר", "category": "dashboard"},
        {"language": "he", "key": "dashboard.plant_suggestion", "value": "הצעת נטיעה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.harvest", "value": "קציר", "category": "dashboard"},
        {"language": "he", "key": "dashboard.plant", "value": "נטיעה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.high_demand_reason", "value": "גידול בביקוש גבוה למחזור מכירה הבא", "category": "dashboard"},
        
        # Priority levels - English
        {"language": "en", "key": "dashboard.priority_high", "value": "High Priority", "category": "dashboard"},
        {"language": "en", "key": "dashboard.priority_medium", "value": "Medium Priority", "category": "dashboard"},
        {"language": "en", "key": "dashboard.priority_low", "value": "Low Priority", "category": "dashboard"},
        {"language": "en", "key": "dashboard.expected_harvest", "value": "Expected Harvest", "category": "dashboard"},
        {"language": "en", "key": "dashboard.market_demand", "value": "Market Demand", "category": "dashboard"},
        
        # Priority levels - Hebrew
        {"language": "he", "key": "dashboard.priority_high", "value": "עדיפות גבוהה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.priority_medium", "value": "עדיפות בינונית", "category": "dashboard"},
        {"language": "he", "key": "dashboard.priority_low", "value": "עדיפות נמוכה", "category": "dashboard"},
        {"language": "he", "key": "dashboard.expected_harvest", "value": "קציר צפוי", "category": "dashboard"},
        {"language": "he", "key": "dashboard.market_demand", "value": "ביקוש שוק", "category": "dashboard"},
    ]


if __name__ == "__main__":
    seed_translations()
