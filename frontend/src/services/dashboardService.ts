import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface DashboardSummary {
  total_farms: number
  total_beds: number
  total_plantings: number
  next_selling_date: string | null
  days_until_next_selling: number | null
}

export interface UpcomingHarvest {
  id: number
  crop_name: string
  bed_name: string
  line_name: string
  expected_harvest_date: string
  days_until_harvest: number
  expected_quantity: number
  planting_id: number
}

export interface PlantingSuggestion {
  bed_id: number
  bed_name: string
  line_id: number
  line_name: string
  available_date: string
  suggested_crop: string
  reason: string
}

export interface DashboardData {
  summary: DashboardSummary
  upcoming_harvests: UpcomingHarvest[]
  planting_suggestions: PlantingSuggestion[]
}

export const dashboardService = {
  async getDashboardData(farmId?: number, weeksAhead: number = 2): Promise<DashboardData> {
    const params = new URLSearchParams()
    if (farmId) params.append('farm_id', farmId.toString())
    params.append('weeks_ahead', weeksAhead.toString())
    
    const response = await axios.get(`${API_BASE_URL}/dashboard/?${params.toString()}`)
    return response.data
  },

  async markHarvested(
    plantingId: number,
    harvestedQuantity: number,
    qualityRating?: number,
    notes?: string
  ): Promise<{ message: string; harvest_id: number }> {
    const response = await axios.post(`${API_BASE_URL}/dashboard/harvests/${plantingId}/mark-harvested`, {
      harvested_quantity: harvestedQuantity,
      quality_rating: qualityRating,
      notes: notes,
    })
    return response.data
  },
} 