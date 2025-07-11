import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface TranslationResponse {
  translations: Record<string, string>
}

export class TranslationService {
  static async getTranslations(language: string): Promise<Record<string, string>> {
    try {
      const response = await axios.get<TranslationResponse>(`${API_BASE_URL}/translations/${language}`)
      return response.data.translations
    } catch (error) {
      console.error('Error fetching translations:', error)
      return {}
    }
  }

  static async getTranslationsByCategory(category: string, language: string): Promise<Record<string, string>> {
    try {
      const response = await axios.get<TranslationResponse>(`${API_BASE_URL}/translations/category/${category}/${language}`)
      return response.data.translations
    } catch (error) {
      console.error('Error fetching translations by category:', error)
      return {}
    }
  }

  static async createTranslation(translation: {
    language: string
    key: string
    value: string
    category?: string
  }): Promise<any> {
    try {
      const response = await axios.post(`${API_BASE_URL}/translations/`, translation)
      return response.data
    } catch (error) {
      console.error('Error creating translation:', error)
      throw error
    }
  }

  static async updateTranslation(id: number, updates: {
    value?: string
    category?: string
    is_active?: boolean
  }): Promise<any> {
    try {
      const response = await axios.put(`${API_BASE_URL}/translations/${id}`, updates)
      return response.data
    } catch (error) {
      console.error('Error updating translation:', error)
      throw error
    }
  }

  static async createBulkTranslations(translations: Array<{
    language: string
    key: string
    value: string
    category?: string
  }>): Promise<any[]> {
    try {
      const response = await axios.post(`${API_BASE_URL}/translations/bulk`, {
        translations
      })
      return response.data
    } catch (error) {
      console.error('Error creating bulk translations:', error)
      throw error
    }
  }
} 