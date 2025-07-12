# Planting Recommendations - Quick Reference

## Algorithm Overview

The planting recommendation system uses a weighted scoring algorithm to suggest optimal crops for available planting lines.

### Scoring Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Market Demand | 40% | Predefined demand scores (0.0-1.0) |
| Seasonal Suitability | 30% | Season-appropriate crops |
| Market Timing | 30% | Alignment with selling dates |
| Historical Yield | Bonus | Past performance bonus |
| Crop Diversity | Bonus | Prevents over-planting |

### Priority Levels

| Score Range | Priority | Color | Description |
|-------------|----------|-------|-------------|
| ≥ 0.8 | High | Red | Urgent recommendations |
| ≥ 0.6 | Medium | Yellow | Good opportunities |
| < 0.6 | Low | Green | Acceptable options |

## Crop Growth Cycles

| Crop | Days to Harvest | Market Demand |
|------|----------------|---------------|
| Lettuce | 45 | 0.9 (High) |
| Spinach | 40 | 0.8 (High) |
| Kale | 55 | 0.7 (Medium) |
| Arugula | 35 | 0.6 (Medium) |
| Basil | 60 | 0.8 (High) |
| Cilantro | 50 | 0.7 (Medium) |
| Mint | 70 | 0.5 (Low) |
| Parsley | 75 | 0.6 (Medium) |
| Chard | 60 | 0.6 (Medium) |
| Mustard Greens | 45 | 0.5 (Low) |
| Bok Choy | 50 | 0.7 (Medium) |
| Radish | 30 | 0.6 (Medium) |
| Carrot | 70 | 0.8 (High) |
| Beet | 60 | 0.6 (Medium) |
| Turnip | 50 | 0.5 (Low) |

## Seasonal Preferences

### Spring (Mar-May)
- Lettuce, Spinach, Arugula, Radish, Peas

### Summer (Jun-Aug)
- Basil, Cilantro, Mint, Chard, Bok Choy

### Fall (Sep-Nov)
- Kale, Spinach, Mustard Greens, Turnip, Carrot

### Winter (Dec-Feb)
- Kale, Spinach, Chard, Mustard Greens

## API Usage

### Get Recommendations
```bash
GET /api/v1/dashboard/?weeks_ahead=2&farm_id=1
```

### Response Structure
```json
{
  "planting_suggestions": [
    {
      "bed_id": 1,
      "bed_name": "Bed A",
      "line_id": 1,
      "line_name": "Line 1",
      "suggested_crop": "Lettuce",
      "reason": "High market demand; Perfect timing for market",
      "priority": "high",
      "expected_harvest_date": "2024-02-22T10:00:00",
      "market_demand_score": 0.9
    }
  ]
}
```

## Configuration

### Market Demand Scores
```python
# In get_market_demand_scores()
"Lettuce": 0.9,    # High demand
"Spinach": 0.8,    # High demand
"Kale": 0.7,       # Medium demand
"Mint": 0.5,       # Low demand
```

### Growth Cycles
```python
# In get_crop_growth_cycles()
"Lettuce": 45,     # 45 days to harvest
"Spinach": 40,     # 40 days to harvest
"Kale": 55,        # 55 days to harvest
```

### Seasonal Preferences
```python
# In get_seasonal_crop_preferences()
"spring": ["Lettuce", "Spinach", "Arugula", "Radish", "Peas"],
"summer": ["Basil", "Cilantro", "Mint", "Chard", "Bok Choy"],
```

## Frontend Display

### Priority Badges
- 🔴 High Priority: Urgent recommendations
- 🟡 Medium Priority: Good opportunities  
- 🟢 Low Priority: Acceptable options

### Information Display
- **Expected Harvest Date**: When crop will be ready
- **Market Demand Score**: Percentage and level (High/Medium/Low)
- **Detailed Reasoning**: Why this crop was recommended

## Troubleshooting

### No Recommendations
- Check if lines are available (no active plantings)
- Verify selling schedules exist
- Ensure crops are defined in growth cycles

### Low Priority Scores
- Review market demand scores
- Check seasonal preferences
- Verify timing alignment with selling dates

### Poor Timing
- Confirm growth cycles are accurate
- Check selling schedule dates
- Adjust weeks_ahead parameter

## Quick Commands

### Test Recommendations
```bash
# Get recommendations for next 2 weeks
curl "http://localhost:8000/api/v1/dashboard/?weeks_ahead=2"

# Get recommendations for specific farm
curl "http://localhost:8000/api/v1/dashboard/?farm_id=1&weeks_ahead=4"
```

### Update Configuration
```python
# Modify market demand scores
def get_market_demand_scores():
    return {
        "Lettuce": 0.9,  # Adjust based on market research
        "Spinach": 0.8,
        # ... add more crops
    }

# Modify growth cycles
def get_crop_growth_cycles():
    return {
        "Lettuce": 45,  # Adjust based on growing conditions
        "Spinach": 40,
        # ... add more crops
    }
```

## Key Functions

### Core Functions
- `get_crop_growth_cycles()` - Crop growth cycle data
- `get_seasonal_crop_preferences()` - Seasonal crop preferences
- `get_market_demand_scores()` - Market demand scores
- `get_current_season()` - Current season detection
- `find_available_lines()` - Find available planting lines
- `calculate_planting_recommendations()` - Main algorithm

### Scoring Logic
1. **Market Demand**: 40% of total score
2. **Seasonal Suitability**: 30% of total score
3. **Market Timing**: 30% of total score
4. **Historical Yield**: Bonus points (up to 20%)
5. **Crop Diversity**: Bonus points (10%)

## Future Enhancements

1. **Weather Integration** - Include weather forecasts
2. **Pest/Disease Risk** - Consider historical patterns
3. **Soil Conditions** - Factor in soil type and fertility
4. **Labor Availability** - Consider planting/harvesting labor
5. **Equipment Constraints** - Factor in available machinery
6. **Cost Analysis** - Include seed costs and profit margins
7. **Succession Planning** - Plan continuous harvest cycles
8. **Market Price Trends** - Include price forecasting 