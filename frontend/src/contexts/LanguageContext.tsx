import { createContext, useContext, useState, ReactNode, useEffect } from 'react'
import { TranslationService } from '../services/translationService'

export type Language = 'en' | 'he'

interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string) => string
  isRTL: boolean
  isLoading: boolean
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

// Local fallback translations
const fallbackTranslations = {
  en: {
    // Navigation
    'nav.dashboard': 'Dashboard',
    'nav.farms': 'Farms',
    'nav.crops': 'Crops',
    'nav.plantings': 'Plantings',
    'nav.scheduler': 'Scheduler',
    
    // Dashboard
    'dashboard.title': 'Dashboard',
    'dashboard.total_farms': 'Total Farms',
    'dashboard.active_crops': 'Active Crops',
    'dashboard.plantings': 'Plantings',
    'dashboard.revenue': 'Revenue',
    'dashboard.recent_plantings': 'Recent Plantings',
    'dashboard.upcoming_harvests': 'Upcoming Harvests',
    'dashboard.planted_days_ago': 'Planted {days} days ago',
    'dashboard.planted_week_ago': 'Planted 1 week ago',
    'dashboard.ready_in_weeks': 'Ready in {weeks} weeks',
    
    // Hierarchy terms
    'hierarchy.farm': 'Farm',
    'hierarchy.bed': 'Bed',
    'hierarchy.line': 'Line',
    'hierarchy.farms': 'Farms',
    'hierarchy.beds': 'Beds',
    'hierarchy.lines': 'Lines',
    'hierarchy.add_farm': 'Add Farm',
    'hierarchy.add_bed': 'Add Bed',
    'hierarchy.add_line': 'Add Line',
    'hierarchy.edit_farm': 'Edit Farm',
    'hierarchy.edit_bed': 'Edit Bed',
    'hierarchy.edit_line': 'Edit Line',
    'hierarchy.delete_farm': 'Delete Farm',
    'hierarchy.delete_bed': 'Delete Bed',
    'hierarchy.delete_line': 'Delete Line',
    
    // Common
    'common.loading': 'Loading...',
    'common.error': 'Error',
    'common.save': 'Save',
    'common.cancel': 'Cancel',
    'common.edit': 'Edit',
    'common.delete': 'Delete',
    'common.add': 'Add',
    'common.search': 'Search',
    'common.name': 'Name',
    'common.description': 'Description',
    'common.location': 'Location',
    'common.area': 'Area',
    'common.position': 'Position',
    'common.quantity': 'Quantity',
    'common.notes': 'Notes',
    
    // Language
    'language.english': 'English',
    'language.hebrew': 'עברית',
    'language.switch': 'Switch Language',
    
    // Placeholder content
    'farms.title': 'Farms',
    'farms.coming_soon': 'Farm management coming soon...',
    'crops.title': 'Crops',
    'crops.coming_soon': 'Crop management coming soon...',
    'plantings.title': 'Plantings',
    'plantings.coming_soon': 'Planting management coming soon...',
    'scheduler.title': 'Scheduler',
    'scheduler.coming_soon': 'Planting scheduler coming soon...',
    // Crops
    'crops.tomatoes': 'Tomatoes',
    'crops.lettuce': 'Lettuce',
    'crops.carrots': 'Carrots',
    'crops.spinach': 'Spinach',
    'crops.cucumbers': 'Cucumbers',
    'crops.peppers': 'Peppers',
    'crops.onions': 'Onions',
    'crops.potatoes': 'Potatoes',
    'crops.broccoli': 'Broccoli',
    'crops.cauliflower': 'Cauliflower',
    'crops.cabbage': 'Cabbage',
    'crops.kale': 'Kale',
    'crops.radishes': 'Radishes',
    'crops.beets': 'Beets',
    'crops.corn': 'Corn',
    'crops.beans': 'Beans',
    'crops.peas': 'Peas',
    'crops.zucchini': 'Zucchini',
    'crops.eggplant': 'Eggplant',
    'crops.squash': 'Squash',
    'crops.pumpkin': 'Pumpkin',
    'crops.melons': 'Melons',
    'crops.strawberries': 'Strawberries',
    'crops.herbs': 'Herbs',
  },
  he: {
    // Navigation
    'nav.dashboard': 'לוח בקרה',
    'nav.farms': 'חוות',
    'nav.crops': 'גידולים',
    'nav.plantings': 'זריעות',
    'nav.scheduler': 'תזמון',
    
    // Dashboard
    'dashboard.title': 'לוח בקרה',
    'dashboard.total_farms': 'סה"כ חוות',
    'dashboard.active_crops': 'גידולים פעילים',
    'dashboard.plantings': 'זריעות',
    'dashboard.revenue': 'הכנסות',
    'dashboard.recent_plantings': 'זריעות אחרונות',
    'dashboard.upcoming_harvests': 'קטיפים קרובים',
    'dashboard.planted_days_ago': 'נזרע לפני {days} ימים',
    'dashboard.planted_week_ago': 'נזרע לפני שבוע',
    'dashboard.ready_in_weeks': 'מוכן בעוד {weeks} שבועות',
    
    // Hierarchy terms
    'hierarchy.farm': 'חווה',
    'hierarchy.bed': 'ערוגה',
    'hierarchy.line': 'שורה',
    'hierarchy.farms': 'חוות',
    'hierarchy.beds': 'ערוגות',
    'hierarchy.lines': 'שורות',
    'hierarchy.add_farm': 'הוסף חווה',
    'hierarchy.add_bed': 'הוסף ערוגה',
    'hierarchy.add_line': 'הוסף שורה',
    'hierarchy.edit_farm': 'ערוך חווה',
    'hierarchy.edit_bed': 'ערוך ערוגה',
    'hierarchy.edit_line': 'ערוך שורה',
    'hierarchy.delete_farm': 'מחק חווה',
    'hierarchy.delete_bed': 'מחק ערוגה',
    'hierarchy.delete_line': 'מחק שורה',
    
    // Common
    'common.loading': 'טוען...',
    'common.error': 'שגיאה',
    'common.save': 'שמור',
    'common.cancel': 'ביטול',
    'common.edit': 'ערוך',
    'common.delete': 'מחק',
    'common.add': 'הוסף',
    'common.search': 'חיפוש',
    'common.name': 'שם',
    'common.description': 'תיאור',
    'common.location': 'מיקום',
    'common.area': 'שטח',
    'common.position': 'מיקום',
    'common.quantity': 'כמות',
    'common.notes': 'הערות',
    
    // Language
    'language.english': 'English',
    'language.hebrew': 'עברית',
    'language.switch': 'החלף שפה',
    
    // Placeholder content
    'farms.title': 'חוות',
    'farms.coming_soon': 'ניהול חוות בקרוב...',
    'crops.title': 'גידולים',
    'crops.coming_soon': 'ניהול גידולים בקרוב...',
    'plantings.title': 'זריעות',
    'plantings.coming_soon': 'ניהול זריעות בקרוב...',
    'scheduler.title': 'תזמון',
    'scheduler.coming_soon': 'תזמון זריעות בקרוב...',
    // Crops
    'crops.tomatoes': 'עגבניות',
    'crops.lettuce': 'חסה',
    'crops.carrots': 'גזר',
    'crops.spinach': 'תרד',
    'crops.cucumbers': 'מלפפונים',
    'crops.peppers': 'פלפלים',
    'crops.onions': 'בצלים',
    'crops.potatoes': 'תפוחי אדמה',
    'crops.broccoli': 'ברוקולי',
    'crops.cauliflower': 'כרובית',
    'crops.cabbage': 'כרוב',
    'crops.kale': 'קייל',
    'crops.radishes': 'צנון',
    'crops.beets': 'סלק',
    'crops.corn': 'תירס',
    'crops.beans': 'שעועית',
    'crops.peas': 'אפונה',
    'crops.zucchini': 'קישוא',
    'crops.eggplant': 'חציל',
    'crops.squash': 'דלעת',
    'crops.pumpkin': 'דלעת עגולה',
    'crops.melons': 'מלונים',
    'crops.strawberries': 'תות שדה',
    'crops.herbs': 'תבלינים',
  }
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>('en')
  const [translations, setTranslations] = useState<Record<string, Record<string, string>>>(fallbackTranslations)
  const [isLoading, setIsLoading] = useState(false)
  
  // Fetch translations from backend when language changes
  useEffect(() => {
    const fetchTranslations = async () => {
      setIsLoading(true)
      try {
        const backendTranslations = await TranslationService.getTranslations(language)
        
        // Merge backend translations with fallback translations
        setTranslations(prev => ({
          ...prev,
          [language]: {
            ...fallbackTranslations[language],
            ...backendTranslations
          }
        }))
      } catch (error) {
        console.error('Failed to fetch translations from backend:', error)
        // Use fallback translations if backend is not available
        setTranslations(prev => ({
          ...prev,
          [language]: fallbackTranslations[language]
        }))
      } finally {
        setIsLoading(false)
      }
    }
    
    fetchTranslations()
  }, [language])
  
  const t = (key: string): string => {
    const currentTranslations = translations[language] || fallbackTranslations[language]
    return currentTranslations[key] || key
  }
  
  const isRTL = language === 'he'
  
  return (
    <LanguageContext.Provider value={{ language, setLanguage, t, isRTL, isLoading }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
} 