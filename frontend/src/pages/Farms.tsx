import React, { useState, useEffect } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import { farmService, Farm, Bed, Line, FarmCreate, BedCreate, LineCreate } from '../services/farmService'

export function Farms() {
  const { t } = useLanguage()
  const [farms, setFarms] = useState<Farm[]>([])
  const [beds, setBeds] = useState<Bed[]>([])
  const [lines, setLines] = useState<Line[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Modal states
  const [showFarmModal, setShowFarmModal] = useState(false)
  const [showBedModal, setShowBedModal] = useState(false)
  const [showLineModal, setShowLineModal] = useState(false)
  const [selectedFarm, setSelectedFarm] = useState<Farm | null>(null)
  const [selectedBed, setSelectedBed] = useState<Bed | null>(null)
  
  // Form states
  const [farmForm, setFarmForm] = useState<FarmCreate>({
    name: '',
    description: '',
    location: '',
    total_area: undefined,
    is_active: true
  })
  
  const [bedForm, setBedForm] = useState<BedCreate>({
    name: '',
    description: '',
    farm_id: 0,
    width: undefined,
    length: undefined,
    soil_type: '',
    is_active: true
  })
  
  const [lineForm, setLineForm] = useState<LineCreate>({
    name: '',
    description: '',
    bed_id: 0,
    position: 1,
    length: undefined,
    width: undefined,
    spacing: undefined,
    is_active: true
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [farmsData, bedsData, linesData] = await Promise.all([
        farmService.getFarms(),
        farmService.getBeds(),
        farmService.getLines()
      ])
      setFarms(farmsData)
      setBeds(bedsData)
      setLines(linesData)
    } catch (err) {
      setError('Failed to load data')
      console.error('Error loading data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateFarm = async () => {
    try {
      const newFarm = await farmService.createFarm(farmForm)
      setFarms([...farms, newFarm])
      setFarmForm({
        name: '',
        description: '',
        location: '',
        total_area: undefined,
        is_active: true
      })
      setShowFarmModal(false)
    } catch (err) {
      setError('Failed to create farm')
      console.error('Error creating farm:', err)
    }
  }

  const handleCreateBed = async () => {
    try {
      const newBed = await farmService.createBed(bedForm)
      setBeds([...beds, newBed])
      setBedForm({
        name: '',
        description: '',
        farm_id: 0,
        width: undefined,
        length: undefined,
        soil_type: '',
        is_active: true
      })
      setShowBedModal(false)
    } catch (err) {
      setError('Failed to create bed')
      console.error('Error creating bed:', err)
    }
  }

  const handleCreateLine = async () => {
    try {
      const newLine = await farmService.createLine(lineForm)
      setLines([...lines, newLine])
      setLineForm({
        name: '',
        description: '',
        bed_id: 0,
        position: 1,
        length: undefined,
        width: undefined,
        spacing: undefined,
        is_active: true
      })
      setShowLineModal(false)
    } catch (err) {
      setError('Failed to create line')
      console.error('Error creating line:', err)
    }
  }

  const getBedsForFarm = (farmId: number) => {
    return beds.filter(bed => bed.farm_id === farmId)
  }

  const getLinesForBed = (bedId: number) => {
    return lines.filter(line => line.bed_id === bedId)
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600 mb-4">{error}</p>
        <button 
          onClick={loadData}
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
        <h1 className="text-2xl font-bold text-secondary-900">{t('farms.title')}</h1>
        <button
          onClick={() => setShowFarmModal(true)}
          className="btn btn-primary flex items-center gap-2"
        >
          + {t('farms.add_farm')}
        </button>
      </div>

      {/* Farms List */}
      <div className="grid gap-6">
        {farms.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-secondary-600 mb-4">{t('farms.no_farms')}</p>
            <button
              onClick={() => setShowFarmModal(true)}
              className="btn btn-primary"
            >
              {t('farms.create_first_farm')}
            </button>
          </div>
        ) : (
          farms.map(farm => (
            <div key={farm.id} className="card">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-secondary-900">{farm.name}</h3>
                  {farm.location && (
                    <p className="text-secondary-600 text-sm">{farm.location}</p>
                  )}
                  {farm.description && (
                    <p className="text-secondary-600 text-sm mt-1">{farm.description}</p>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setSelectedFarm(farm)
                      setBedForm({ ...bedForm, farm_id: farm.id })
                      setShowBedModal(true)
                    }}
                    className="btn btn-secondary btn-sm flex items-center gap-1"
                  >
                    + {t('farms.add_bed')}
                  </button>
                </div>
              </div>

              {/* Beds for this farm */}
              <div className="space-y-4">
                {getBedsForFarm(farm.id).length === 0 ? (
                  <div className="text-center py-4 border-2 border-dashed border-secondary-200 rounded-lg">
                    <p className="text-secondary-500 text-sm">{t('farms.no_beds')}</p>
                  </div>
                ) : (
                  getBedsForFarm(farm.id).map(bed => (
                    <div key={bed.id} className="border border-secondary-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h4 className="font-medium text-secondary-900">{bed.name}</h4>
                          {bed.description && (
                            <p className="text-secondary-600 text-sm">{bed.description}</p>
                          )}
                          {(bed.length || bed.width) && (
                            <p className="text-secondary-500 text-xs">
                              {bed.length}m × {bed.width}m
                              {bed.area && ` (${bed.area}m²)`}
                            </p>
                          )}
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => {
                              setSelectedBed(bed)
                              setLineForm({ ...lineForm, bed_id: bed.id })
                              setShowLineModal(true)
                            }}
                            className="btn btn-secondary btn-sm flex items-center gap-1"
                          >
                            + {t('farms.add_line')}
                          </button>
                        </div>
                      </div>

                      {/* Lines for this bed */}
                      <div className="space-y-2">
                        {getLinesForBed(bed.id).length === 0 ? (
                          <div className="text-center py-2 border border-dashed border-secondary-200 rounded">
                            <p className="text-secondary-400 text-xs">{t('farms.no_lines')}</p>
                          </div>
                        ) : (
                          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                            {getLinesForBed(bed.id).map(line => (
                              <div key={line.id} className="bg-secondary-50 p-2 rounded text-sm">
                                <div className="flex justify-between items-center">
                                  <span className="font-medium">{line.name}</span>
                                  <span className="text-secondary-500 text-xs">#{line.position}</span>
                                </div>
                                {line.description && (
                                  <p className="text-secondary-600 text-xs truncate">{line.description}</p>
                                )}
                              </div>
                            ))}
                          </div>
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

      {/* Farm Creation Modal */}
      {showFarmModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-semibold mb-4">{t('farms.create_farm')}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.name')} *
                </label>
                <input
                  type="text"
                  value={farmForm.name}
                  onChange={(e) => setFarmForm({ ...farmForm, name: e.target.value })}
                  className="input w-full"
                  placeholder={t('farms.name_placeholder')}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.location')}
                </label>
                <input
                  type="text"
                  value={farmForm.location || ''}
                  onChange={(e) => setFarmForm({ ...farmForm, location: e.target.value })}
                  className="input w-full"
                  placeholder={t('farms.location_placeholder')}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.description')}
                </label>
                <textarea
                  value={farmForm.description || ''}
                  onChange={(e) => setFarmForm({ ...farmForm, description: e.target.value })}
                  className="input w-full"
                  rows={3}
                  placeholder={t('farms.description_placeholder')}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.total_area')} (m²)
                </label>
                <input
                  type="number"
                  value={farmForm.total_area || ''}
                  onChange={(e) => setFarmForm({ ...farmForm, total_area: e.target.value ? Number(e.target.value) : undefined })}
                  className="input w-full"
                  placeholder="0"
                />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowFarmModal(false)}
                className="btn btn-secondary flex-1"
              >
                {t('common.cancel')}
              </button>
              <button
                onClick={handleCreateFarm}
                disabled={!farmForm.name}
                className="btn btn-primary flex-1"
              >
                {t('common.create')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Bed Creation Modal */}
      {showBedModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-semibold mb-4">{t('farms.create_bed')}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.bed_name')} *
                </label>
                <input
                  type="text"
                  value={bedForm.name}
                  onChange={(e) => setBedForm({ ...bedForm, name: e.target.value })}
                  className="input w-full"
                  placeholder={t('farms.bed_name_placeholder')}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.bed_description')}
                </label>
                <textarea
                  value={bedForm.description || ''}
                  onChange={(e) => setBedForm({ ...bedForm, description: e.target.value })}
                  className="input w-full"
                  rows={2}
                  placeholder={t('farms.bed_description_placeholder')}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('farms.length')} (m)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={bedForm.length || ''}
                    onChange={(e) => setBedForm({ ...bedForm, length: e.target.value ? Number(e.target.value) : undefined })}
                    className="input w-full"
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('farms.width')} (m)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={bedForm.width || ''}
                    onChange={(e) => setBedForm({ ...bedForm, width: e.target.value ? Number(e.target.value) : undefined })}
                    className="input w-full"
                    placeholder="0"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.soil_type')}
                </label>
                <input
                  type="text"
                  value={bedForm.soil_type || ''}
                  onChange={(e) => setBedForm({ ...bedForm, soil_type: e.target.value })}
                  className="input w-full"
                  placeholder={t('farms.soil_type_placeholder')}
                />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowBedModal(false)}
                className="btn btn-secondary flex-1"
              >
                {t('common.cancel')}
              </button>
              <button
                onClick={handleCreateBed}
                disabled={!bedForm.name}
                className="btn btn-primary flex-1"
              >
                {t('common.create')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Line Creation Modal */}
      {showLineModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-semibold mb-4">{t('farms.create_line')}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.line_name')} *
                </label>
                <input
                  type="text"
                  value={lineForm.name}
                  onChange={(e) => setLineForm({ ...lineForm, name: e.target.value })}
                  className="input w-full"
                  placeholder={t('farms.line_name_placeholder')}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-1">
                  {t('farms.line_description')}
                </label>
                <textarea
                  value={lineForm.description || ''}
                  onChange={(e) => setLineForm({ ...lineForm, description: e.target.value })}
                  className="input w-full"
                  rows={2}
                  placeholder={t('farms.line_description_placeholder')}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('farms.position')} *
                  </label>
                  <input
                    type="number"
                    min="1"
                    value={lineForm.position}
                    onChange={(e) => setLineForm({ ...lineForm, position: Number(e.target.value) })}
                    className="input w-full"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('farms.spacing')} (cm)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={lineForm.spacing || ''}
                    onChange={(e) => setLineForm({ ...lineForm, spacing: e.target.value ? Number(e.target.value) : undefined })}
                    className="input w-full"
                    placeholder="0"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('farms.length')} (m)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={lineForm.length || ''}
                    onChange={(e) => setLineForm({ ...lineForm, length: e.target.value ? Number(e.target.value) : undefined })}
                    className="input w-full"
                    placeholder="0"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-secondary-700 mb-1">
                    {t('farms.width')} (m)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={lineForm.width || ''}
                    onChange={(e) => setLineForm({ ...lineForm, width: e.target.value ? Number(e.target.value) : undefined })}
                    className="input w-full"
                    placeholder="0"
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowLineModal(false)}
                className="btn btn-secondary flex-1"
              >
                {t('common.cancel')}
              </button>
              <button
                onClick={handleCreateLine}
                disabled={!lineForm.name}
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