import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

interface Harvest {
  id: number;
  crop_name: string;
  bed_name: string;
  line_name: string;
  harvest_date: string;
  harvested_quantity: number;
  quality_rating?: number;
  days_early_late?: number;
  yield_percentage?: number;
  is_complete: boolean;
}

interface Planting {
  id: number;
  crop_name: string;
  bed_name: string;
  line_name: string;
  planted_date: string;
  expected_harvest_date: string;
  quantity: number;
  is_active: boolean;
}

const Harvests: React.FC = () => {
  const { t } = useLanguage();
  const [harvests, setHarvests] = useState<Harvest[]>([]);
  const [plantings, setPlantings] = useState<Planting[]>([]);
  const [showRecordForm, setShowRecordForm] = useState(false);
  const [selectedPlanting, setSelectedPlanting] = useState<Planting | null>(null);
  const [formData, setFormData] = useState({
    harvest_date: '',
    harvested_quantity: '',
    quality_rating: '',
    notes: '',
    weather_conditions: '',
    harvest_method: '',
    harvested_by: ''
  });

  useEffect(() => {
    fetchHarvests();
    fetchActivePlantings();
  }, []);

  const fetchHarvests = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/v1/harvests/');
      if (response.ok) {
        const data = await response.json();
        setHarvests(data);
      }
    } catch (error) {
      console.error('Error fetching harvests:', error);
    }
  };

  const fetchActivePlantings = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/v1/plantings/?is_active=true');
      if (response.ok) {
        const data = await response.json();
        setPlantings(data);
      }
    } catch (error) {
      console.error('Error fetching plantings:', error);
    }
  };

  const handleRecordHarvest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPlanting) return;

    try {
      const response = await fetch('http://localhost:8001/api/v1/harvests/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          planting_id: selectedPlanting.id,
          farm_id: 1, // Assuming single farm for now
          bed_id: 1, // Will need to get from planting
          line_id: 1, // Will need to get from planting
          crop_id: 1, // Will need to get from planting
          harvest_date: formData.harvest_date,
          harvested_quantity: parseFloat(formData.harvested_quantity),
          quality_rating: formData.quality_rating ? parseInt(formData.quality_rating) : null,
          notes: formData.notes || null,
          weather_conditions: formData.weather_conditions || null,
          harvest_method: formData.harvest_method || null,
          harvested_by: formData.harvested_by || null,
        }),
      });

      if (response.ok) {
        const newHarvest = await response.json();
        setHarvests([newHarvest, ...harvests]);
        setShowRecordForm(false);
        setSelectedPlanting(null);
        setFormData({
          harvest_date: '',
          harvested_quantity: '',
          quality_rating: '',
          notes: '',
          weather_conditions: '',
          harvest_method: '',
          harvested_by: ''
        });
      }
    } catch (error) {
      console.error('Error recording harvest:', error);
    }
  };

  const getTimingStatus = (daysEarlyLate?: number) => {
    if (!daysEarlyLate) return { text: t('harvests.noExpectedDate'), color: 'text-gray-500' };
    if (daysEarlyLate > 0) return { text: t('harvests.early').replace('{days}', daysEarlyLate.toString()), color: 'text-green-600' };
    if (daysEarlyLate < 0) return { text: t('harvests.late').replace('{days}', Math.abs(daysEarlyLate).toString()), color: 'text-red-600' };
    return { text: t('harvests.onTime'), color: 'text-blue-600' };
  };

  const getYieldStatus = (percentage?: number) => {
    if (!percentage) return { text: t('harvests.noExpectedYield'), color: 'text-gray-500' };
    if (percentage > 100) return { text: t('harvests.highYield').replace('{percentage}', percentage.toFixed(1)), color: 'text-green-600' };
    if (percentage < 80) return { text: t('harvests.lowYield').replace('{percentage}', percentage.toFixed(1)), color: 'text-red-600' };
    return { text: t('harvests.expectedYield').replace('{percentage}', percentage.toFixed(1)), color: 'text-blue-600' };
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          {t('harvests.title')}
        </h1>
        <button
          onClick={() => setShowRecordForm(true)}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          {t('harvests.recordHarvest')}
        </button>
      </div>

      {/* Record Harvest Form */}
      {showRecordForm && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">{t('harvests.recordNewHarvest')}</h2>
          <form onSubmit={handleRecordHarvest} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  {t('harvests.selectPlanting')}
                </label>
                <select
                  value={selectedPlanting?.id || ''}
                  onChange={(e) => {
                    const planting = plantings.find(p => p.id === parseInt(e.target.value));
                    setSelectedPlanting(planting || null);
                  }}
                  className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
                  required
                >
                  <option value="">{t('harvests.selectPlanting')}</option>
                  {plantings.map((planting) => (
                    <option key={planting.id} value={planting.id}>
                      {planting.crop_name} - {planting.bed_name} - {planting.line_name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  {t('harvests.harvestDate')}
                </label>
                <input
                  type="datetime-local"
                  value={formData.harvest_date}
                  onChange={(e) => setFormData({...formData, harvest_date: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  {t('harvests.quantity')} (kg)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.harvested_quantity}
                  onChange={(e) => setFormData({...formData, harvested_quantity: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  {t('harvests.qualityRating')} (1-5)
                </label>
                <input
                  type="number"
                  min="1"
                  max="5"
                  value={formData.quality_rating}
                  onChange={(e) => setFormData({...formData, quality_rating: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  {t('harvests.weatherConditions')}
                </label>
                <input
                  type="text"
                  value={formData.weather_conditions}
                  onChange={(e) => setFormData({...formData, weather_conditions: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  {t('harvests.harvestMethod')}
                </label>
                <select
                  value={formData.harvest_method}
                  onChange={(e) => setFormData({...formData, harvest_method: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
                >
                  <option value="">{t('harvests.selectMethod')}</option>
                  <option value="manual">{t('harvests.manual')}</option>
                  <option value="machine">{t('harvests.machine')}</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                {t('harvests.notes')}
              </label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
                rows={3}
                className="w-full p-2 border border-gray-300 rounded-lg dark:bg-gray-700 dark:border-gray-600"
              />
            </div>

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => setShowRecordForm(false)}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-700"
              >
                {t('common.cancel')}
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                {t('harvests.recordHarvest')}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Harvests List */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold">{t('harvests.recentHarvests')}</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.crop')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.location')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.date')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.quantity')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.timing')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.yield')}
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  {t('harvests.quality')}
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {harvests.map((harvest) => {
                const timingStatus = getTimingStatus(harvest.days_early_late);
                const yieldStatus = getYieldStatus(harvest.yield_percentage);
                
                return (
                  <tr key={harvest.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                      {harvest.crop_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                      {harvest.bed_name} - {harvest.line_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                      {new Date(harvest.harvest_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                      {harvest.harvested_quantity} kg
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={timingStatus.color}>
                        {timingStatus.text}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={yieldStatus.color}>
                        {yieldStatus.text}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                      {harvest.quality_rating ? `${harvest.quality_rating}/5` : '-'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Harvests; 