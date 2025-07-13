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
        
        # Farms - English
        {"language": "en", "key": "farms.title", "value": "Farms", "category": "farms"},
        {"language": "en", "key": "farms.add_farm", "value": "Add Farm", "category": "farms"},
        {"language": "en", "key": "farms.create_farm", "value": "Create Farm", "category": "farms"},
        {"language": "en", "key": "farms.name", "value": "Name", "category": "farms"},
        {"language": "en", "key": "farms.name_placeholder", "value": "Enter farm name", "category": "farms"},
        {"language": "en", "key": "farms.location", "value": "Location", "category": "farms"},
        {"language": "en", "key": "farms.location_placeholder", "value": "Enter farm location", "category": "farms"},
        {"language": "en", "key": "farms.description", "value": "Description", "category": "farms"},
        {"language": "en", "key": "farms.description_placeholder", "value": "Enter farm description", "category": "farms"},
        {"language": "en", "key": "farms.total_area", "value": "Total Area", "category": "farms"},
        {"language": "en", "key": "farms.no_farms", "value": "No farms yet", "category": "farms"},
        {"language": "en", "key": "farms.create_first_farm", "value": "Create Your First Farm", "category": "farms"},
        {"language": "en", "key": "farms.add_bed", "value": "Add Bed", "category": "farms"},
        {"language": "en", "key": "farms.create_bed", "value": "Create Bed", "category": "farms"},
        {"language": "en", "key": "farms.bed_name", "value": "Bed Name", "category": "farms"},
        {"language": "en", "key": "farms.bed_name_placeholder", "value": "Enter bed name", "category": "farms"},
        {"language": "en", "key": "farms.bed_description", "value": "Bed Description", "category": "farms"},
        {"language": "en", "key": "farms.bed_description_placeholder", "value": "Enter bed description", "category": "farms"},
        {"language": "en", "key": "farms.length", "value": "Length", "category": "farms"},
        {"language": "en", "key": "farms.width", "value": "Width", "category": "farms"},
        {"language": "en", "key": "farms.soil_type", "value": "Soil Type", "category": "farms"},
        {"language": "en", "key": "farms.soil_type_placeholder", "value": "Enter soil type", "category": "farms"},
        {"language": "en", "key": "farms.no_beds", "value": "No beds yet", "category": "farms"},
        {"language": "en", "key": "farms.add_line", "value": "Add Line", "category": "farms"},
        {"language": "en", "key": "farms.create_line", "value": "Create Line", "category": "farms"},
        {"language": "en", "key": "farms.line_name", "value": "Line Name", "category": "farms"},
        {"language": "en", "key": "farms.line_name_placeholder", "value": "Enter line name", "category": "farms"},
        {"language": "en", "key": "farms.line_description", "value": "Line Description", "category": "farms"},
        {"language": "en", "key": "farms.line_description_placeholder", "value": "Enter line description", "category": "farms"},
        {"language": "en", "key": "farms.position", "value": "Position", "category": "farms"},
        {"language": "en", "key": "farms.spacing", "value": "Spacing", "category": "farms"},
        {"language": "en", "key": "farms.no_lines", "value": "No lines yet", "category": "farms"},
        
        # Farms - Hebrew
        {"language": "he", "key": "farms.title", "value": "חוות", "category": "farms"},
        {"language": "he", "key": "farms.add_farm", "value": "הוסף חווה", "category": "farms"},
        {"language": "he", "key": "farms.create_farm", "value": "צור חווה", "category": "farms"},
        {"language": "he", "key": "farms.name", "value": "שם", "category": "farms"},
        {"language": "he", "key": "farms.name_placeholder", "value": "הכנס שם חווה", "category": "farms"},
        {"language": "he", "key": "farms.location", "value": "מיקום", "category": "farms"},
        {"language": "he", "key": "farms.location_placeholder", "value": "הכנס מיקום חווה", "category": "farms"},
        {"language": "he", "key": "farms.description", "value": "תיאור", "category": "farms"},
        {"language": "he", "key": "farms.description_placeholder", "value": "הכנס תיאור חווה", "category": "farms"},
        {"language": "he", "key": "farms.total_area", "value": "שטח כולל", "category": "farms"},
        {"language": "he", "key": "farms.no_farms", "value": "אין חוות עדיין", "category": "farms"},
        {"language": "he", "key": "farms.create_first_farm", "value": "צור את החווה הראשונה שלך", "category": "farms"},
        {"language": "he", "key": "farms.add_bed", "value": "הוסף ערוגה", "category": "farms"},
        {"language": "he", "key": "farms.create_bed", "value": "צור ערוגה", "category": "farms"},
        {"language": "he", "key": "farms.bed_name", "value": "שם ערוגה", "category": "farms"},
        {"language": "he", "key": "farms.bed_name_placeholder", "value": "הכנס שם ערוגה", "category": "farms"},
        {"language": "he", "key": "farms.bed_description", "value": "תיאור ערוגה", "category": "farms"},
        {"language": "he", "key": "farms.bed_description_placeholder", "value": "הכנס תיאור ערוגה", "category": "farms"},
        {"language": "he", "key": "farms.length", "value": "אורך", "category": "farms"},
        {"language": "he", "key": "farms.width", "value": "רוחב", "category": "farms"},
        {"language": "he", "key": "farms.soil_type", "value": "סוג אדמה", "category": "farms"},
        {"language": "he", "key": "farms.soil_type_placeholder", "value": "הכנס סוג אדמה", "category": "farms"},
        {"language": "he", "key": "farms.no_beds", "value": "אין ערוגות עדיין", "category": "farms"},
        {"language": "he", "key": "farms.add_line", "value": "הוסף שורה", "category": "farms"},
        {"language": "he", "key": "farms.create_line", "value": "צור שורה", "category": "farms"},
        {"language": "he", "key": "farms.line_name", "value": "שם שורה", "category": "farms"},
        {"language": "he", "key": "farms.line_name_placeholder", "value": "הכנס שם שורה", "category": "farms"},
        {"language": "he", "key": "farms.line_description", "value": "תיאור שורה", "category": "farms"},
        {"language": "he", "key": "farms.line_description_placeholder", "value": "הכנס תיאור שורה", "category": "farms"},
        {"language": "he", "key": "farms.position", "value": "מיקום", "category": "farms"},
        {"language": "he", "key": "farms.spacing", "value": "מרווח", "category": "farms"},
        {"language": "he", "key": "farms.no_lines", "value": "אין שורות עדיין", "category": "farms"},
        
        # Plantings - English
        {"language": "en", "key": "plantings.title", "value": "Growing", "category": "plantings"},
        {"language": "en", "key": "plantings.add_planting", "value": "Add Planting", "category": "plantings"},
        {"language": "en", "key": "plantings.create_planting", "value": "Create Planting", "category": "plantings"},
        {"language": "en", "key": "plantings.farm", "value": "Farm", "category": "plantings"},
        {"language": "en", "key": "plantings.select_farm", "value": "Select Farm", "category": "plantings"},
        {"language": "en", "key": "plantings.bed", "value": "Bed", "category": "plantings"},
        {"language": "en", "key": "plantings.select_bed", "value": "Select Bed", "category": "plantings"},
        {"language": "en", "key": "plantings.line", "value": "Line", "category": "plantings"},
        {"language": "en", "key": "plantings.select_line", "value": "Select Line", "category": "plantings"},
        {"language": "en", "key": "plantings.crop", "value": "Crop", "category": "plantings"},
        {"language": "en", "key": "plantings.select_crop", "value": "Select Crop", "category": "plantings"},
        {"language": "en", "key": "plantings.planting_date", "value": "Planting Date", "category": "plantings"},
        {"language": "en", "key": "plantings.expected_harvest_date", "value": "Expected Harvest Date", "category": "plantings"},
        {"language": "en", "key": "plantings.quantity", "value": "Quantity", "category": "plantings"},
        {"language": "en", "key": "plantings.spacing", "value": "Spacing", "category": "plantings"},
        {"language": "en", "key": "plantings.notes", "value": "Notes", "category": "plantings"},
        {"language": "en", "key": "plantings.notes_placeholder", "value": "Enter planting notes", "category": "plantings"},
        {"language": "en", "key": "plantings.plants", "value": "plants", "category": "plantings"},
        {"language": "en", "key": "plantings.planted", "value": "Planted", "category": "plantings"},
        {"language": "en", "key": "plantings.expected_harvest", "value": "Expected Harvest", "category": "plantings"},
        {"language": "en", "key": "plantings.active", "value": "Active", "category": "plantings"},
        {"language": "en", "key": "plantings.no_farms", "value": "No farms yet", "category": "plantings"},
        {"language": "en", "key": "plantings.create_farm_first", "value": "Create a farm first", "category": "plantings"},
        {"language": "en", "key": "plantings.no_beds", "value": "No beds yet", "category": "plantings"},
        {"language": "en", "key": "plantings.no_lines", "value": "No lines yet", "category": "plantings"},
        {"language": "en", "key": "plantings.no_plantings", "value": "No plantings yet", "category": "plantings"},
        
        # Plantings - Hebrew
        {"language": "he", "key": "plantings.title", "value": "גידול", "category": "plantings"},
        {"language": "he", "key": "plantings.add_planting", "value": "הוסף נטיעה", "category": "plantings"},
        {"language": "he", "key": "plantings.create_planting", "value": "צור נטיעה", "category": "plantings"},
        {"language": "he", "key": "plantings.farm", "value": "חווה", "category": "plantings"},
        {"language": "he", "key": "plantings.select_farm", "value": "בחר חווה", "category": "plantings"},
        {"language": "he", "key": "plantings.bed", "value": "ערוגה", "category": "plantings"},
        {"language": "he", "key": "plantings.select_bed", "value": "בחר ערוגה", "category": "plantings"},
        {"language": "he", "key": "plantings.line", "value": "שורה", "category": "plantings"},
        {"language": "he", "key": "plantings.select_line", "value": "בחר שורה", "category": "plantings"},
        {"language": "he", "key": "plantings.crop", "value": "גידול", "category": "plantings"},
        {"language": "he", "key": "plantings.select_crop", "value": "בחר גידול", "category": "plantings"},
        {"language": "he", "key": "plantings.planting_date", "value": "תאריך נטיעה", "category": "plantings"},
        {"language": "he", "key": "plantings.expected_harvest_date", "value": "תאריך קציר צפוי", "category": "plantings"},
        {"language": "he", "key": "plantings.quantity", "value": "כמות", "category": "plantings"},
        {"language": "he", "key": "plantings.spacing", "value": "מרווח", "category": "plantings"},
        {"language": "he", "key": "plantings.notes", "value": "הערות", "category": "plantings"},
        {"language": "he", "key": "plantings.notes_placeholder", "value": "הכנס הערות נטיעה", "category": "plantings"},
        {"language": "he", "key": "plantings.plants", "value": "צמחים", "category": "plantings"},
        {"language": "he", "key": "plantings.planted", "value": "נטוע", "category": "plantings"},
        {"language": "he", "key": "plantings.expected_harvest", "value": "קציר צפוי", "category": "plantings"},
        {"language": "he", "key": "plantings.active", "value": "פעיל", "category": "plantings"},
        {"language": "he", "key": "plantings.no_farms", "value": "אין חוות עדיין", "category": "plantings"},
        {"language": "he", "key": "plantings.create_farm_first", "value": "צור חווה קודם", "category": "plantings"},
        {"language": "he", "key": "plantings.no_beds", "value": "אין ערוגות עדיין", "category": "plantings"},
        {"language": "he", "key": "plantings.no_lines", "value": "אין שורות עדיין", "category": "plantings"},
        {"language": "he", "key": "plantings.no_plantings", "value": "אין נטיעות עדיין", "category": "plantings"},
        
        # Common - English
        {"language": "en", "key": "common.retry", "value": "Retry", "category": "common"},
        {"language": "en", "key": "common.create", "value": "Create", "category": "common"},
        {"language": "en", "key": "common.cancel", "value": "Cancel", "category": "common"},
        {"language": "en", "key": "common.delete", "value": "Delete", "category": "common"},
        {"language": "en", "key": "farms.confirm_delete", "value": "Are you sure you want to delete this farm? This action cannot be undone.", "category": "farms"},
        {"language": "en", "key": "plantings.confirm_delete", "value": "Are you sure you want to delete this planting? This action cannot be undone.", "category": "plantings"},
        # Common - Hebrew
        {"language": "he", "key": "common.retry", "value": "נסה שוב", "category": "common"},
        {"language": "he", "key": "common.create", "value": "צור", "category": "common"},
        {"language": "he", "key": "common.cancel", "value": "ביטול", "category": "common"},
        {"language": "he", "key": "common.delete", "value": "מחק", "category": "common"},
        {"language": "he", "key": "farms.confirm_delete", "value": "האם אתה בטוח שברצונך למחוק את החווה הזו? פעולה זו אינה ניתנת לביטול.", "category": "farms"},
        {"language": "he", "key": "plantings.confirm_delete", "value": "האם אתה בטוח שברצונך למחוק את הנטיעה הזו? פעולה זו אינה ניתנת לביטול.", "category": "plantings"},
    ]


if __name__ == "__main__":
    seed_translations()
