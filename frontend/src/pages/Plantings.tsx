import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useLanguage } from '../contexts/LanguageContext'
import { farmService, Farm, Bed, Line } from '../services/farmService'

interface Crop {
  id: number
  name: string
  category: string
  growth_cycle_days: number
  expected_yield_per_plant: number
  is_active: boolean
}

interface Planting {
  id: number
  farm_id: number
  bed_id: number
  line_id: number
  crop_id: number
  planting_date: string
  expected_harvest_date: string
  quantity: number
  spacing: number
  notes: string
  is_active: boolean
  created_at: string
  updated_at: string
}

interface PlantingCreate {
  farm_id: number
  bed_id: number
  line_id: number
  crop_id: number
  planting_date: string
  expected_harvest_date: string
  quantity: number
  spacing: number
  notes: string
  is_active: boolean
}

export function Plantings() {
  const { t } = useLanguage()
  const queryClient = useQueryClient()
  
  // Modal states
  const [showPlantingModal, setShowPlantingModal] = useState(false)
  const [selectedFarm, setSelectedFarm] = useState<Farm | null>(null)
  const [selectedBed, setSelectedBed] = useState<Bed | null>(null)
  
  // Form states
  const [plantingForm, setPlantingForm] = useState<PlantingCreate>({
    farm_id: 0,
    bed_id: 0,
    line_id: 0,
    crop_id: 0,
    planting_date: '',
    expected_harvest_date: '',
    quantity: 0,
    spacing: 0,
    notes: '',
    is_active: true
  })

  // Queries
  const { data: farms = [], isLoading: farmsLoading, error: farmsError } = useQuery(
    ['farms'],
    farmService.getFarms
  )

  const { data: beds = [], isLoading: bedsLoading, error: bedsError } = useQuery(
    ['beds'],
    farmService.getBeds
  )

  const { data: lines = [], isLoading: linesLoading, error: linesError } = useQuery(
    ['lines'],
    farmService.getLines
  )

  const { data: crops = [], isLoading: cropsLoading, error: cropsError } = useQuery(
    ['crops'],
    async () => {
      const response = await fetch('http://localhost:8000/api/v1/crops/')
      return response.json()
    }
  )

  const { data: plantings = [], isLoading: plantingsLoading, error: plantingsError } = useQuery(
    ['plantings'],
    async () => {
      const response = await fetch('http://localhost:8000/api/v1/plantings/')
      return response.json()
    }
  )

  // Mutations
  const createPlantingMutation = useMutation(
    async (planting: PlantingCreate) => {
      const response = await fetch('http://localhost:8000/api/v1/plantings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(planting),
      })
      return response.json()
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['plantings'])
        setPlantingForm({
          farm_id: 0,
          bed_id: 0,
          line_id: 0,
          crop_id: 0,
          planting_date: '',
          expected_harvest_date: '',
          quantity: 0,
          spacing: 0,
          notes: '',
          is_active: true
        })
        setShowPlantingModal(false)
      }
    }
  )

  const deletePlantingMutation = useMutation(farmService.deletePlanting, {
    onSuccess: () => {
      queryClient.invalidateQueries(['plantings'])
    }
  })

  const handleCreatePlanting = () => {
    createPlantingMutation.mutate(plantingForm)
  }

  const getBedsForFarm = (farmId: number) => {
    return (beds as Bed[]).filter(bed => bed.farm_id === farmId)
  }

  const getLinesForBed = (bedId: number) => {
    return (lines as Line[]).filter(line => line.bed_id === bedId)
  }

  const getPlantingsForLine = (lineId: number) => {
    return (plantings as Planting[]).filter(planting => planting.line_id === lineId && planting.is_active)
  }

  const getCropName = (cropId: number) => {
    const crop = (crops as Crop[]).find(c => c.id === cropId)
    return crop ? crop.name : 'Unknown Crop'
  }

  const getFarmName = (farmId: number) => {
    const farm = (farms as Farm[]).find(f => f.id === farmId)
    return farm ? farm.name : 'Unknown Farm'
  }

  const getBedName = (bedId: number) => {
    const bed = (beds as Bed[]).find(b => b.id === bedId)
    return bed ? bed.name : 'Unknown Bed'
  }

  const getLineName = (lineId: number) => {
    const line = (lines as Line[]).find(l => l.id === lineId)
    return line ? line.name : 'Unknown Line'
  }

  const calculateExpectedHarvestDate = (plantingDate: string, cropId: number) => {
    const crop = (crops as Crop[]).find(c => c.id === cropId)
    if (!crop) return ''
    
    const date = new Date(plantingDate)
    date.setDate(date.getDate() + crop.growth_cycle_days)
    return date.toISOString().split('T')[0]
  }

  const handleCropChange = (cropId: number) => {
    const crop = (crops as Crop[]).find(c => c.id === cropId)
    if (crop && plantingForm.planting_date) {
      const expectedDate = calculateExpectedHarvestDate(plantingForm.planting_date, cropId)
      setPlantingForm({ ...plantingForm, crop_id: cropId, expected_harvest_date: expectedDate })
    } else {
      setPlantingForm({ ...plantingForm, crop_id: cropId })
    }
  }

  const handlePlantingDateChange = (date: string) => {
    setPlantingForm({ ...plantingForm, planting_date: date })
    if (plantingForm.crop_id) {
      const expectedDate = calculateExpectedHarvestDate(date, plantingForm.crop_id)
      setPlantingForm({ ...plantingForm, planting_date: date, expected_harvest_date: expectedDate })
    }
  }

  const isLoading = farmsLoading || bedsLoading || linesLoading || cropsLoading || plantingsLoading
  const error = farmsError || bedsError || linesError || cropsError || plantingsError

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">Failed to load data</p>
        <button 
          onClick={() => queryClient.invalidateQueries()}
          className="btn btn-primary"
        >
          {t('common.retry')}
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-secondary-900">{t('plantings.title')}</h1>
        <button
          onClick={() => setShowPlantingModal(true)}
          className="btn btn-primary flex items-center gap-2"
        >
          + {t('plantings.add_planting')}
        </button>
      </div>

      {/* Plantings Overview */}
      <div className="grid gap-6">
        {farms.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-secondary-600 mb-4">{t('plantings.no_farms')}</p>
            <p className="text-secondary-500 text-sm">{t('plantings.create_farm_first')}</p>
          </div>
        ) : (
          farms.map(farm => (
            <div key={farm.id} className="card">
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-secondary-900">{farm.name}</h3>
                {farm.location && (
                  <p className="text-secondary-600 text-sm">{farm.location}</p>
                )}
              </div>

              {/* Beds and Lines with Plantings */}
              <div className="space-y-4">
                {getBedsForFarm(farm.id).length === 0 ? (
                  <div className="text-center py-4 border-2 border-dashed border-secondary-200 rounded-lg">
                    <p className="text-secondary-500 text-sm">{t('plantings.no_beds')}</p>
                  </div>
                ) : (
                  getBedsForFarm(farm.id).map(bed => (
                    <div key={bed.id} className="border border-secondary-200 rounded-lg p-4">
                      <div className="mb-3">
                        <h4 className="font-medium text-secondary-900">{bed.name}</h4>
                        {bed.description && (
                          <p className="text-secondary-600 text-sm">{bed.description}</p>
                        )}
                      </div>

                      {/* Lines with Plantings */}
                      <div className="space-y-3">
                        {getLinesForBed(bed.id).length === 0 ? (
                          <div className="text-center py-2 border border-dashed border-secondary-200 rounded">
                            <p className="text-secondary-400 text-xs">{t('plantings.no_lines')}</p>
                          </div>
                        ) : (
                          getLinesForBed(bed.id).map(line => {
                            const linePlantings = getPlantingsForLine(line.id)
                            return (
                              <div key={line.id} className="bg-secondary-50 p-3 rounded">
                                <div className="flex justify-between items-center mb-2">
                                  <span className="font-medium text-sm">{line.name}</span>
                                  <span className="text-secondary-500 text-xs">#{line.position}</span>
                                </div>
                                
                                {/* Plantings in this line */}
                                {linePlantings.length === 0 ? (
                                  <div className="text-center py-2 border border-dashed border-secondary-200 rounded bg-white">
                                    <p className="text-secondary-400 text-xs">{t('plantings.no_plantings')}</p>
                                  </div>
                                ) : (
                                  <div className="space-y-2">
                                    {linePlantings.map(planting => (
                                      <div key={planting.id} className="bg-white p-2 rounded border">
                                        <div className="flex justify-between items-start">
                                          <div className="flex-1">
                                            <p className="font-medium text-sm">{getCropName(planting.crop_id)}</p>
                                            <p className="text-secondary-600 text-xs">
                                              {t('plantings.planted')}: {new Date(planting.planting_date).toLocaleDateString()}
                                            </p>
                                            <p className="text-secondary-600 text-xs">
                                              {t('plantings.expected_harvest')}: {new Date(planting.expected_harvest_date).toLocaleDateString()}
                                            </p>
                                            <p className="text-secondary-500 text-xs">
                                              {t('plantings.quantity')}: {planting.quantity} {t('plantings.plants')}
                                            </p>
                                          </div>
                                          <div className="text-right flex flex-col gap-2">
                                            <span className="inline-block px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                                              {t('plantings.active')}
                                            </span>
                                            <button
                                              onClick={() => {
                                                if (window.confirm(t('plantings.confirm_delete'))) {
                                                  deletePlantingMutation.mutate(planting.id)
                                                }
                                              }}
                                              className="btn btn-danger btn-xs mt-2"
                                            >
                                              {t('common.delete')}
                                            </button>
                                          </div>
                                        </div>
                                        {planting.notes && (
                                          <p className="text-secondary-500 text-xs mt-1">{planting.notes}</p>
                                        )}
                                      </div>
                                    ))}
                                  </div>
                                )}
                              </div>
                            )
                          })
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Planting Creation Modal */}
      {showPlantingModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-semibold mb-4">{t('plantings.create_planting')}</h2>
            <div className="space-y-4">
              {/* Farm Selection */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.farm')} *
                </label>
                <select
                  value={plantingForm.farm_id}
                  onChange={(e) => {
                    const farmId = Number(e.target.value)
                    setPlantingForm({ ...plantingForm, farm_id: farmId, bed_id: 0, line_id: 0 })
                  }}
                  className="input w-full"
                >
                  <option value={0}>{t('plantings.select_farm')}</option>
                  {farms.map(farm => (
                    <option key={farm.id} value={farm.id}>{farm.name}</option>
                  ))}
                </select>
              </div>

              {/* Bed Selection */}
              {plantingForm.farm_id > 0 && (
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('plantings.bed')} *
                  </label>
                  <select
                    value={plantingForm.bed_id}
                    onChange={(e) => {
                      const bedId = Number(e.target.value)
                      setPlantingForm({ ...plantingForm, bed_id: bedId, line_id: 0 })
                    }}
                    className="input w-full"
                  >
                    <option value={0}>{t('plantings.select_bed')}</option>
                    {getBedsForFarm(plantingForm.farm_id).map(bed => (
                      <option key={bed.id} value={bed.id}>{bed.name}</option>
                    ))}
                  </select>
                </div>
              )}

              {/* Line Selection */}
              {plantingForm.bed_id > 0 && (
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('plantings.line')} *
                  </label>
                  <select
                    value={plantingForm.line_id}
                    onChange={(e) => setPlantingForm({ ...plantingForm, line_id: Number(e.target.value) })}
                    className="input w-full"
                  >
                    <option value={0}>{t('plantings.select_line')}</option>
                    {getLinesForBed(plantingForm.bed_id).map(line => (
                      <option key={line.id} value={line.id}>{line.name} (#{line.position})</option>
                    ))}
                  </select>
                </div>
              )}

              {/* Crop Selection */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.crop')} *
                </label>
                <select
                  value={plantingForm.crop_id}
                  onChange={(e) => handleCropChange(Number(e.target.value))}
                  className="input w-full"
                >
                  <option value={0}>{t('plantings.select_crop')}</option>
                  {crops.map((crop: Crop) => (
                    <option key={crop.id} value={crop.id}>
                      {crop.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Planting Date */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.planting_date')} *
                </label>
                <input
                  type="date"
                  value={plantingForm.planting_date}
                  onChange={(e) => handlePlantingDateChange(e.target.value)}
                  className="input w-full"
                />
              </div>

              {/* Expected Harvest Date */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.expected_harvest_date')} *
                </label>
                <input
                  type="date"
                  value={plantingForm.expected_harvest_date}
                  onChange={(e) => setPlantingForm({ ...plantingForm, expected_harvest_date: e.target.value })}
                  className="input w-full"
                />
              </div>

              {/* Quantity */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.quantity')} *
                </label>
                <input
                  type="number"
                  min="1"
                  value={plantingForm.quantity}
                  onChange={(e) => setPlantingForm({ ...plantingForm, quantity: Number(e.target.value) })}
                  className="input w-full"
                  placeholder="0"
                />
              </div>

              {/* Spacing */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.spacing')} (cm)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={plantingForm.spacing}
                  onChange={(e) => setPlantingForm({ ...plantingForm, spacing: Number(e.target.value) })}
                  className="input w-full"
                  placeholder="0"
                />
              </div>

              {/* Notes */}
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('plantings.notes')}
                </label>
                <textarea
                  value={plantingForm.notes}
                  onChange={(e) => setPlantingForm({ ...plantingForm, notes: e.target.value })}
                  className="input w-full"
                  rows={3}
                  placeholder={t('plantings.notes_placeholder')}
                />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowPlantingModal(false)}
                className="btn btn-secondary flex-1"
              >
                {t('common.cancel')}
              </button>
              <button
                onClick={handleCreatePlanting}
                disabled={!plantingForm.farm_id || !plantingForm.bed_id || !plantingForm.line_id || !plantingForm.crop_id || !plantingForm.planting_date || !plantingForm.expected_harvest_date || plantingForm.quantity <= 0}
                className="btn btn-primary flex-1"
              >
                {t('common.create')}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 