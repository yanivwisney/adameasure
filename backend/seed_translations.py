#!/usr/bin/env python3
"""
Seed the database with initial translations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.translation import Translation

def seed_translations():
    """Seed the database with initial translations"""
    db = SessionLocal()
    
    # Initial translations data
    translations_data = [
        # Hebrew custom terms
        {"language": "he", "key": "farm.harvest", "value": "קטיף", "category": "farm_terms"},
        {"language": "he", "key": "farm.planting", "value": "זריעה", "category": "farm_terms"},
        {"language": "he", "key": "farm.growing", "value": "גידול", "category": "farm_terms"},
        {"language": "he", "key": "farm.bed", "value": "ערוגה", "category": "farm_terms"},
        {"language": "he", "key": "farm.field", "value": "שדה", "category": "farm_terms"},
        {"language": "he", "key": "farm.greenhouse", "value": "חממה", "category": "farm_terms"},
        {"language": "he", "key": "farm.irrigation", "value": "השקיה", "category": "farm_terms"},
        {"language": "he", "key": "farm.fertilizer", "value": "דשן", "category": "farm_terms"},
        {"language": "he", "key": "farm.pesticide", "value": "חומר הדברה", "category": "farm_terms"},
        {"language": "he", "key": "farm.organic", "value": "אורגני", "category": "farm_terms"},
        {"language": "he", "key": "farm.yield", "value": "יבול", "category": "farm_terms"},
        {"language": "he", "key": "farm.quality", "value": "איכות", "category": "farm_terms"},
        
        # Crop names in Hebrew
        {"language": "he", "key": "crops.tomatoes", "value": "עגבניות", "category": "crops"},
        {"language": "he", "key": "crops.lettuce", "value": "חסה", "category": "crops"},
        {"language": "he", "key": "crops.carrots", "value": "גזר", "category": "crops"},
        {"language": "he", "key": "crops.spinach", "value": "תרד", "category": "crops"},
        {"language": "he", "key": "crops.cucumbers", "value": "מלפפונים", "category": "crops"},
        {"language": "he", "key": "crops.peppers", "value": "פלפלים", "category": "crops"},
        {"language": "he", "key": "crops.onions", "value": "בצלים", "category": "crops"},
        {"language": "he", "key": "crops.potatoes", "value": "תפוחי אדמה", "category": "crops"},
        {"language": "he", "key": "crops.broccoli", "value": "ברוקולי", "category": "crops"},
        {"language": "he", "key": "crops.cauliflower", "value": "כרובית", "category": "crops"},
        {"language": "he", "key": "crops.cabbage", "value": "כרוב", "category": "crops"},
        {"language": "he", "key": "crops.kale", "value": "קייל", "category": "crops"},
        {"language": "he", "key": "crops.radishes", "value": "צנון", "category": "crops"},
        {"language": "he", "key": "crops.beets", "value": "סלק", "category": "crops"},
        {"language": "he", "key": "crops.corn", "value": "תירס", "category": "crops"},
        {"language": "he", "key": "crops.beans", "value": "שעועית", "category": "crops"},
        {"language": "he", "key": "crops.peas", "value": "אפונה", "category": "crops"},
        {"language": "he", "key": "crops.zucchini", "value": "קישוא", "category": "crops"},
        {"language": "he", "key": "crops.eggplant", "value": "חציל", "category": "crops"},
        {"language": "he", "key": "crops.squash", "value": "דלעת", "category": "crops"},
        {"language": "he", "key": "crops.pumpkin", "value": "דלעת עגולה", "category": "crops"},
        {"language": "he", "key": "crops.melons", "value": "מלונים", "category": "crops"},
        {"language": "he", "key": "crops.strawberries", "value": "תות שדה", "category": "crops"},
        {"language": "he", "key": "crops.herbs", "value": "תבלינים", "category": "crops"},
        
        # English farm terms
        {"language": "en", "key": "farm.harvest", "value": "Harvest", "category": "farm_terms"},
        {"language": "en", "key": "farm.planting", "value": "Planting", "category": "farm_terms"},
        {"language": "en", "key": "farm.growing", "value": "Growing", "category": "farm_terms"},
        {"language": "en", "key": "farm.bed", "value": "Bed", "category": "farm_terms"},
        {"language": "en", "key": "farm.field", "value": "Field", "category": "farm_terms"},
        {"language": "en", "key": "farm.greenhouse", "value": "Greenhouse", "category": "farm_terms"},
        {"language": "en", "key": "farm.irrigation", "value": "Irrigation", "category": "farm_terms"},
        {"language": "en", "key": "farm.fertilizer", "value": "Fertilizer", "category": "farm_terms"},
        {"language": "en", "key": "farm.pesticide", "value": "Pesticide", "category": "farm_terms"},
        {"language": "en", "key": "farm.organic", "value": "Organic", "category": "farm_terms"},
        {"language": "en", "key": "farm.yield", "value": "Yield", "category": "farm_terms"},
        {"language": "en", "key": "farm.quality", "value": "Quality", "category": "farm_terms"},
        
        # English crop names
        {"language": "en", "key": "crops.tomatoes", "value": "Tomatoes", "category": "crops"},
        {"language": "en", "key": "crops.lettuce", "value": "Lettuce", "category": "crops"},
        {"language": "en", "key": "crops.carrots", "value": "Carrots", "category": "crops"},
        {"language": "en", "key": "crops.spinach", "value": "Spinach", "category": "crops"},
        {"language": "en", "key": "crops.cucumbers", "value": "Cucumbers", "category": "crops"},
        {"language": "en", "key": "crops.peppers", "value": "Peppers", "category": "crops"},
        {"language": "en", "key": "crops.onions", "value": "Onions", "category": "crops"},
        {"language": "en", "key": "crops.potatoes", "value": "Potatoes", "category": "crops"},
        {"language": "en", "key": "crops.broccoli", "value": "Broccoli", "category": "crops"},
        {"language": "en", "key": "crops.cauliflower", "value": "Cauliflower", "category": "crops"},
        {"language": "en", "key": "crops.cabbage", "value": "Cabbage", "category": "crops"},
        {"language": "en", "key": "crops.kale", "value": "Kale", "category": "crops"},
        {"language": "en", "key": "crops.radishes", "value": "Radishes", "category": "crops"},
        {"language": "en", "key": "crops.beets", "value": "Beets", "category": "crops"},
        {"language": "en", "key": "crops.corn", "value": "Corn", "category": "crops"},
        {"language": "en", "key": "crops.beans", "value": "Beans", "category": "crops"},
        {"language": "en", "key": "crops.peas", "value": "Peas", "category": "crops"},
        {"language": "en", "key": "crops.zucchini", "value": "Zucchini", "category": "crops"},
        {"language": "en", "key": "crops.eggplant", "value": "Eggplant", "category": "crops"},
        {"language": "en", "key": "crops.squash", "value": "Squash", "category": "crops"},
        {"language": "en", "key": "crops.pumpkin", "value": "Pumpkin", "category": "crops"},
        {"language": "en", "key": "crops.melons", "value": "Melons", "category": "crops"},
        {"language": "en", "key": "crops.strawberries", "value": "Strawberries", "category": "crops"},
        {"language": "en", "key": "crops.herbs", "value": "Herbs", "category": "crops"},
    ]
    
    try:
        # Clear existing translations
        db.query(Translation).delete()
        db.commit()
        
        # Add new translations
        for translation_data in translations_data:
            translation = Translation(**translation_data)
            db.add(translation)
        
        db.commit()
        print("✅ Translations seeded successfully!")
        print(f"📝 Added {len(translations_data)} translations")
        
    except Exception as e:
        print(f"❌ Error seeding translations: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_translations() 