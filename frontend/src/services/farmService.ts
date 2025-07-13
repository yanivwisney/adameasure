import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface Farm {
  id: number
  name: string
  description?: string
  location?: string
  total_area?: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface FarmCreate {
  name: string
  description?: string
  location?: string
  total_area?: number
  is_active?: boolean
}

export interface FarmUpdate {
  name?: string
  description?: string
  location?: string
  total_area?: number
  is_active?: boolean
}

export interface Bed {
  id: number
  name: string
  description?: string
  farm_id: number
  width?: number
  length?: number
  area?: number
  soil_type?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface BedCreate {
  name: string
  description?: string
  farm_id: number
  width?: number
  length?: number
  soil_type?: string
  is_active?: boolean
}

export interface BedUpdate {
  name?: string
  description?: string
  width?: number
  length?: number
  soil_type?: string
  is_active?: boolean
}

export interface Line {
  id: number
  name: string
  description?: string
  bed_id: number
  position: number
  length?: number
  width?: number
  spacing?: number
  area?: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface LineCreate {
  name: string
  description?: string
  bed_id: number
  position: number
  length?: number
  width?: number
  spacing?: number
  is_active?: boolean
}

export interface LineUpdate {
  name?: string
  description?: string
  position?: number
  length?: number
  width?: number
  spacing?: number
  is_active?: boolean
}

export const farmService = {
  // Farm operations
  async getFarms(): Promise<Farm[]> {
    const response = await axios.get(`${API_BASE_URL}/farms/`)
    return response.data
  },

  async getFarm(farmId: number): Promise<Farm> {
    const response = await axios.get(`${API_BASE_URL}/farms/${farmId}`)
    return response.data
  },

  async createFarm(farm: FarmCreate): Promise<Farm> {
    const response = await axios.post(`${API_BASE_URL}/farms/`, farm)
    return response.data
  },

  async updateFarm(farmId: number, farm: FarmUpdate): Promise<Farm> {
    const response = await axios.put(`${API_BASE_URL}/farms/${farmId}`, farm)
    return response.data
  },

  async deleteFarm(farmId: number): Promise<void> {
    await axios.delete(`${API_BASE_URL}/farms/${farmId}`)
  },

  // Bed operations
  async getBeds(farmId?: number): Promise<Bed[]> {
    const params = farmId ? `?farm_id=${farmId}` : ''
    const response = await axios.get(`${API_BASE_URL}/beds/${params}`)
    return response.data
  },

  async getBed(bedId: number): Promise<Bed> {
    const response = await axios.get(`${API_BASE_URL}/beds/${bedId}`)
    return response.data
  },

  async createBed(bed: BedCreate): Promise<Bed> {
    const response = await axios.post(`${API_BASE_URL}/beds/`, bed)
    return response.data
  },

  async updateBed(bedId: number, bed: BedUpdate): Promise<Bed> {
    const response = await axios.put(`${API_BASE_URL}/beds/${bedId}`, bed)
    return response.data
  },

  async deleteBed(bedId: number): Promise<void> {
    await axios.delete(`${API_BASE_URL}/beds/${bedId}`)
  },

  // Line operations
  async getLines(bedId?: number): Promise<Line[]> {
    const params = bedId ? `?bed_id=${bedId}` : ''
    const response = await axios.get(`${API_BASE_URL}/lines/${params}`)
    return response.data
  },

  async getLinesByBed(bedId: number): Promise<Line[]> {
    const response = await axios.get(`${API_BASE_URL}/lines/bed/${bedId}`)
    return response.data
  },

  async getLine(lineId: number): Promise<Line> {
    const response = await axios.get(`${API_BASE_URL}/lines/${lineId}`)
    return response.data
  },

  async createLine(line: LineCreate): Promise<Line> {
    const response = await axios.post(`${API_BASE_URL}/lines/`, line)
    return response.data
  },

  async updateLine(lineId: number, line: LineUpdate): Promise<Line> {
    const response = await axios.put(`${API_BASE_URL}/lines/${lineId}`, line)
    return response.data
  },

  async deleteLine(lineId: number): Promise<void> {
    await axios.delete(`${API_BASE_URL}/lines/${lineId}`)
  },
} 