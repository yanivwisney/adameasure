import { BarChart3, Building2, Calendar, Grid } from 'lucide-react'
import { useLanguage } from '../contexts/LanguageContext'

export function Dashboard() {
  const { t, isRTL } = useLanguage()

  return (
    <div>
      <h1 className="text-2xl font-bold text-secondary-900 mb-6">{t('dashboard.title')}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Building2 className="h-6 w-6 text-primary-600" />
            </div>
            <div className={isRTL ? 'mr-4' : 'ml-4'}>
              <p className="text-sm font-medium text-secondary-600">{t('hierarchy.farms')}</p>
              <p className="text-2xl font-bold text-secondary-900">2</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Grid className="h-6 w-6 text-green-600" />
            </div>
            <div className={isRTL ? 'mr-4' : 'ml-4'}>
              <p className="text-sm font-medium text-secondary-600">{t('hierarchy.beds')}</p>
              <p className="text-2xl font-bold text-secondary-900">8</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Calendar className="h-6 w-6 text-blue-600" />
            </div>
            <div className={isRTL ? 'mr-4' : 'ml-4'}>
              <p className="text-sm font-medium text-secondary-600">{t('dashboard.plantings')}</p>
              <p className="text-2xl font-bold text-secondary-900">12</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <BarChart3 className="h-6 w-6 text-purple-600" />
            </div>
            <div className={isRTL ? 'mr-4' : 'ml-4'}>
              <p className="text-sm font-medium text-secondary-600">{t('dashboard.revenue')}</p>
              <p className="text-2xl font-bold text-secondary-900">$2,450</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold text-secondary-900 mb-4">{t('dashboard.recent_plantings')}</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
              <div>
                <p className="font-medium text-secondary-900">{t('crops.tomatoes')}</p>
                <p className="text-sm text-secondary-600">{t('dashboard.planted_days_ago').replace('{days}', '3')}</p>
              </div>
              <div className="text-right">
                <span className="text-sm text-primary-600 font-medium">Farm A - Bed 1 - Line 2</span>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
              <div>
                <p className="font-medium text-secondary-900">{t('crops.lettuce')}</p>
                <p className="text-sm text-secondary-600">{t('dashboard.planted_week_ago')}</p>
              </div>
              <div className="text-right">
                <span className="text-sm text-primary-600 font-medium">Farm B - Bed 2 - Line 1</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="card">
          <h2 className="text-lg font-semibold text-secondary-900 mb-4">{t('dashboard.upcoming_harvests')}</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div>
                <p className="font-medium text-secondary-900">{t('crops.carrots')}</p>
                <p className="text-sm text-secondary-600">{t('dashboard.ready_in_weeks').replace('{weeks}', '2')}</p>
              </div>
              <div className="text-right">
                <span className="text-sm text-green-600 font-medium">Farm A - Bed 3 - Line 1</span>
              </div>
            </div>
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div>
                <p className="font-medium text-secondary-900">{t('crops.spinach')}</p>
                <p className="text-sm text-secondary-600">{t('dashboard.ready_in_weeks').replace('{weeks}', '3')}</p>
              </div>
              <div className="text-right">
                <span className="text-sm text-yellow-600 font-medium">Farm B - Bed 1 - Line 3</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 