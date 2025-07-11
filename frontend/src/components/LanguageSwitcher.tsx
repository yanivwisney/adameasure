import { Globe } from 'lucide-react'
import { useLanguage } from '../contexts/LanguageContext'

export function LanguageSwitcher() {
  const { language, setLanguage, t } = useLanguage()

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'he' : 'en')
  }

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900 rounded-lg transition-colors duration-200"
      title={t('language.switch')}
    >
      <Globe size={16} />
      <span className="hidden sm:inline">
        {language === 'en' ? t('language.hebrew') : t('language.english')}
      </span>
      <span className="sm:hidden">
        {language === 'en' ? 'עב' : 'EN'}
      </span>
    </button>
  )
} 