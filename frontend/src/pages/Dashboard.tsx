import { BarChart3, Building2, Calendar, Grid, Clock, Scissors, Sprout } from 'lucide-react'
import { useLanguage } from '../contexts/LanguageContext'
import { useState, useEffect } from 'react'
import { dashboardService, DashboardData, UpcomingHarvest } from '../services/dashboardService'

export function Dashboard() {
  const { t, isRTL } = useLanguage()
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [weeksAhead, setWeeksAhead] = useState(2)

  useEffect(() => {
    fetchDashboardData()
  }, [weeksAhead])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await dashboardService.getDashboardData(undefined, weeksAhead)
      setDashboardData(data)
    } catch (err) {
      console.error('Error fetching dashboard data:', err)
      setError('Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const handleMarkHarvested = async (plantingId: number, expectedQuantity: number) => {
    try {
      await dashboardService.markHarvested(plantingId, expectedQuantity)
      // Refresh dashboard data
      await fetchDashboardData()
    } catch (err) {
      console.error('Error marking harvest:', err)
      setError('Failed to mark harvest')
    }
  }

  const formatCountdown = (days: number | null) => {
    if (days === null) return t('dashboard.no_upcoming_sales')
    if (days === 0) return t('dashboard.today')
    if (days === 1) return t('dashboard.tomorrow')
    return t('dashboard.days').replace('{days}', days.toString())
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-secondary-600">{t('common.loading')}</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-600">{error}</div>
      </div>
    )
  }

  if (!dashboardData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-secondary-600">No data available</div>
      </div>
    )
  }

  const { summary, upcoming_harvests, planting_suggestions } = dashboardData

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-secondary-900">{t('dashboard.title')}</h1>
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-secondary-600">
            {t('dashboard.weeks_ahead')}:
          </label>
          <select
            value={weeksAhead}
            onChange={(e) => setWeeksAhead(Number(e.target.value))}
            className="border border-secondary-300 rounded-lg px-3 py-1 text-sm"
          >
            <option value={1}>1 week</option>
            <option value={2}>2 weeks</option>
            <option value={4}>4 weeks</option>
            <option value={8}>8 weeks</option>
          </select>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Building2 className="h-6 w-6 text-primary-600" />
            </div>
            <div className={isRTL ? 'mr-4' : 'ml-4'}>
              <p className="text-sm font-medium text-secondary-600">{t('hierarchy.farms')}</p>
              <p className="text-2xl font-bold text-secondary-900">{summary.total_farms}</p>
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
              <p className="text-2xl font-bold text-secondary-900">{summary.total_beds}</p>
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
              <p className="text-2xl font-bold text-secondary-900">{summary.total_plantings}</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Clock className="h-6 w-6 text-purple-600" />
            </div>
            <div className={isRTL ? 'mr-4' : 'ml-4'}>
              <p className="text-sm font-medium text-secondary-600">{t('dashboard.next_selling')}</p>
              <p className="text-2xl font-bold text-secondary-900">
                {formatCountdown(summary.days_until_next_selling)}
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-secondary-900">
              {t('dashboard.upcoming_harvests')}
            </h2>
            <span className="text-sm text-secondary-500">
              {t('dashboard.upcoming_count').replace('{count}', upcoming_harvests.length.toString())}
            </span>
          </div>
          <div className="space-y-3">
            {upcoming_harvests.length === 0 ? (
              <p className="text-secondary-500 text-center py-4">{t('dashboard.no_upcoming_harvests')}</p>
            ) : (
              upcoming_harvests.map((harvest) => (
                <div key={harvest.id} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{harvest.crop_name}</p>
                    <p className="text-sm text-secondary-600">
                      {harvest.bed_name} - {harvest.line_name}
                    </p>
                    <p className="text-sm text-secondary-600">
                      {t('dashboard.ready_in_days').replace('{days}', harvest.days_until_harvest.toString())}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-green-600 font-medium">
                      {harvest.expected_quantity} kg
                    </span>
                    <button
                      onClick={() => handleMarkHarvested(harvest.planting_id, harvest.expected_quantity)}
                      className="flex items-center gap-1 px-3 py-1 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors"
                      title={t('dashboard.mark_harvested')}
                    >
                      <Scissors size={14} />
                      {t('dashboard.harvest')}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
        
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-secondary-900">
              {t('dashboard.planting_suggestions')}
            </h2>
            <span className="text-sm text-secondary-500">
              {t('dashboard.available_count').replace('{count}', planting_suggestions.length.toString())}
            </span>
          </div>
          <div className="space-y-3">
            {planting_suggestions.length === 0 ? (
              <p className="text-secondary-500 text-center py-4">{t('dashboard.no_planting_suggestions')}</p>
            ) : (
              planting_suggestions.map((suggestion, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{suggestion.bed_name} - {suggestion.line_name}</p>
                    <p className="text-sm text-secondary-600">
                      {t('dashboard.suggested')}: {suggestion.suggested_crop}
                    </p>
                    <p className="text-sm text-secondary-600">
                      {suggestion.reason}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-blue-600 font-medium">
                      {t('dashboard.available')}
                    </span>
                    <button
                      className="flex items-center gap-1 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
                      title={t('dashboard.plant_suggestion')}
                    >
                      <Sprout size={14} />
                      {t('dashboard.plant')}
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 