import { useLanguage } from '../contexts/LanguageContext'

export function Plantings() {
  const { t } = useLanguage()

  return (
    <div>
      <h1 className="text-2xl font-bold text-secondary-900 mb-6">{t('plantings.title')}</h1>
      <div className="card">
        <p className="text-secondary-600">{t('plantings.coming_soon')}</p>
      </div>
    </div>
  )
} 