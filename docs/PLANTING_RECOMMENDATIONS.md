# Planting Recommendations System

## Overview

The planting recommendations system is an intelligent algorithm that analyzes multiple factors to provide data-driven suggestions for crop planting. It helps farmers optimize their planting decisions by considering market demand, seasonal factors, growth cycles, and historical performance.

## How It Works

### 1. Data Collection & Analysis

The system analyzes several data sources to make informed recommendations:

- **Available Space**: Finds lines that are currently empty and available for planting
- **Historical Performance**: Analyzes past harvest data to predict future yields
- **Market Timing**: Considers upcoming selling dates to align harvests with market opportunities
- **Seasonal Factors**: Considers which crops perform best in different seasons

### 2. Scoring Algorithm

Each crop is scored based on multiple weighted factors:

#### Market Demand (40% weight)
- Predefined demand scores for each crop (0.0-1.0)
- High-demand crops like Lettuce (0.9) and Spinach (0.8) get higher scores
- Lower-demand crops like Mint (0.5) get lower scores

#### Seasonal Suitability (30% weight)
- **Spring**: Lettuce, Spinach, Arugula, Radish, Peas
- **Summer**: Basil, Cilantro, Mint, Chard, Bok Choy
- **Fall**: Kale, Spinach, Mustard Greens, Turnip, Carrot
- **Winter**: Kale, Spinach, Chard, Mustard Greens

#### Market Timing (30% weight)
- Calculates if harvest date aligns with upcoming selling dates
- Perfect timing (within 1 week): 100% score
- Good timing (within 2 weeks): 80% score
- Poor timing: 0% score

#### Historical Yield Bonus (up to 20% bonus)
- Analyzes past harvest data for each crop
- Crops with historically good yields get bonus points
- Helps learn from farm-specific performance

#### Diversity Bonus (10% bonus)
- Prevents over-planting the same crop
- Encourages crop rotation and diversity
- Reduces risk from crop-specific issues

### 3. Growth Cycle Management

The system includes growth cycle data for 15+ crops:

```python
growth_cycles = {
    "Lettuce": 45,      # 45 days to harvest
    "Spinach": 40,      # 40 days to harvest
    "Kale": 55,         # 55 days to harvest
    "Arugula": 35,      # 35 days to harvest
    "Basil": 60,        # 60 days to harvest
    "Cilantro": 50,     # 50 days to harvest
    "Mint": 70,         # 70 days to harvest
    "Parsley": 75,      # 75 days to harvest
    "Chard": 60,        # 60 days to harvest
    "Mustard Greens": 45, # 45 days to harvest
    "Bok Choy": 50,     # 50 days to harvest
    "Radish": 30,       # 30 days to harvest
    "Carrot": 70,       # 70 days to harvest
    "Beet": 60,         # 60 days to harvest
    "Turnip": 50,       # 50 days to harvest
}
```

### 4. Priority Classification

Recommendations are classified by priority:

- **High Priority (score ≥ 0.8)**: Red badge, urgent recommendations
- **Medium Priority (score ≥ 0.6)**: Yellow badge, good opportunities
- **Low Priority (score < 0.6)**: Green badge, acceptable options

## Implementation Details

### Core Functions

#### `get_crop_growth_cycles()`
Returns a dictionary mapping crop names to their typical growth cycles in days.

#### `get_seasonal_crop_preferences()`
Returns seasonal crop preferences organized by season.

#### `get_market_demand_scores()`
Returns market demand scores (0.0-1.0) for each crop.

#### `get_current_season()`
Determines the current season based on the current date.

#### `find_available_lines(db, farm_id)`
Finds lines that are currently available for planting by checking for active plantings.

#### `calculate_planting_recommendations(db, available_lines, weeks_ahead)`
The main algorithm that calculates intelligent planting recommendations.

### Algorithm Flow

1. **Data Gathering**
   - Get available lines and beds
   - Fetch upcoming selling dates
   - Retrieve historical harvest data
   - Calculate average yields by crop

2. **Crop Evaluation**
   For each available line and each crop:
   - Calculate market demand score
   - Evaluate seasonal suitability
   - Check market timing alignment
   - Apply historical yield bonus
   - Consider crop diversity

3. **Scoring & Ranking**
   - Combine all factors with weighted scoring
   - Select best crop for each line
   - Assign priority levels
   - Sort by priority and score

4. **Recommendation Generation**
   - Create detailed recommendations with reasoning
   - Include expected harvest dates
   - Provide market demand information

## API Endpoints

### GET `/api/v1/dashboard/`

Returns comprehensive dashboard data including planting recommendations.

**Parameters:**
- `farm_id` (optional): Filter by specific farm
- `weeks_ahead` (default: 2): Number of weeks to look ahead for recommendations

**Response:**
```json
{
  "summary": {
    "total_farms": 1,
    "total_beds": 3,
    "total_plantings": 5,
    "next_selling_date": "2024-01-15T10:00:00",
    "days_until_next_selling": 7
  },
  "upcoming_harvests": [...],
  "planting_suggestions": [
    {
      "bed_id": 1,
      "bed_name": "Bed A",
      "line_id": 1,
      "line_name": "Line 1",
      "available_date": "2024-01-08T10:00:00",
      "suggested_crop": "Lettuce",
      "reason": "High market demand; Perfect timing for market",
      "priority": "high",
      "expected_harvest_date": "2024-02-22T10:00:00",
      "market_demand_score": 0.9
    }
  ]
}
```

## Frontend Display

The enhanced dashboard shows:

- **Priority badges** (High/Medium/Low) with color coding
- **Expected harvest dates** for planning
- **Market demand scores** as percentages
- **Detailed reasoning** for each recommendation
- **Visual indicators** for quick decision making

## Benefits

This system provides:

- **Data-driven decisions** instead of guesswork
- **Optimized timing** for market opportunities
- **Risk reduction** through diversity
- **Learning capability** from historical performance
- **Seasonal awareness** for better crop selection
- **Profit maximization** through demand alignment

## Configuration

### Market Demand Scores
Adjust crop demand scores in `get_market_demand_scores()` based on your market research and customer preferences.

### Growth Cycles
Update crop growth cycles in `get_crop_growth_cycles()` based on your specific growing conditions and crop varieties.

### Seasonal Preferences
Modify seasonal crop preferences in `get_seasonal_crop_preferences()` based on your climate and growing conditions.

### Scoring Weights
Adjust the scoring weights in `calculate_planting_recommendations()`:
- Market demand: 40%
- Seasonal suitability: 30%
- Market timing: 30%
- Historical yield bonus: up to 20%
- Diversity bonus: 10%

## Example Recommendation Process

For an available line, the system:

1. **Evaluates each crop** against all criteria
2. **Calculates composite score** using weighted factors
3. **Selects best crop** for that specific line
4. **Provides detailed reasoning** for the recommendation
5. **Assigns priority level** based on score
6. **Predicts harvest date** and market demand

## Future Enhancements

Potential improvements to consider:

1. **Weather Integration**: Include weather forecasts in recommendations
2. **Pest/Disease Risk**: Consider historical pest and disease patterns
3. **Soil Conditions**: Factor in soil type and fertility
4. **Labor Availability**: Consider planting and harvesting labor requirements
5. **Equipment Constraints**: Factor in available equipment and machinery
6. **Cost Analysis**: Include seed costs and expected profit margins
7. **Succession Planning**: Plan multiple plantings for continuous harvest
8. **Market Price Trends**: Include price forecasting and trends

## Troubleshooting

### Common Issues

1. **No Recommendations**: Check if there are available lines and upcoming selling dates
2. **Low Priority Scores**: Review market demand scores and seasonal preferences
3. **Poor Timing**: Verify growth cycles and selling schedule alignment
4. **Missing Historical Data**: The system works without historical data but improves with it

### Debugging

Enable debug logging to see detailed scoring calculations:

```python
# Add to calculate_planting_recommendations function
print(f"Crop: {crop_name}, Score: {score}, Reason: {reason_parts}")
```

## Contributing

When modifying the recommendation system:

1. Update documentation for any algorithm changes
2. Test with various scenarios and edge cases
3. Consider backward compatibility
4. Add appropriate logging for debugging
5. Update translation keys for new features

## Related Files

- `backend/app/api/endpoints/dashboard.py`: Main recommendation algorithm
- `frontend/src/pages/Dashboard.tsx`: Frontend display logic
- `frontend/src/services/dashboardService.ts`: API service
- `backend/seed_translations.py`: Translation keys for UI elements 