# Documentation

This directory contains comprehensive documentation for the AdamEasure farm management system.

## Documentation Structure

### Core System Documentation

- **[PLANTING_RECOMMENDATIONS.md](./PLANTING_RECOMMENDATIONS.md)** - Detailed explanation of the intelligent planting recommendation system
  - Algorithm overview and scoring system
  - Implementation details and configuration
  - API endpoints and usage examples
  - Troubleshooting and future enhancements

### System Architecture

The farm management system consists of several key components:

1. **Backend API** (FastAPI + SQLAlchemy + PostgreSQL)
   - RESTful API endpoints for all farm operations
   - Database models and relationships
   - Business logic and data processing

2. **Frontend Application** (React + TypeScript + Tailwind)
   - Modern, responsive user interface
   - Real-time dashboard with data visualization
   - Internationalization support (English/Hebrew)

3. **Planting Recommendation Engine**
   - Intelligent algorithm for crop suggestions
   - Market demand analysis
   - Seasonal optimization
   - Historical performance learning

## Key Features

### Dashboard
- Real-time farm overview with key metrics
- Upcoming harvest tracking
- Intelligent planting recommendations
- Market timing optimization

### Harvest Management
- Complete harvest tracking system
- Yield analysis and comparison
- Quality assessment
- Historical performance tracking

### Internationalization
- Full English and Hebrew support
- Dynamic language switching
- Culturally appropriate translations

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### Installation
1. Clone the repository
2. Install backend dependencies: `cd backend && pip install -r requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`
4. Set up the database and run migrations
5. Start the development servers

### Development
- Backend: `cd backend && python start.py`
- Frontend: `cd frontend && npm run dev`

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the backend server is running.

### Key Endpoints
- `GET /api/v1/dashboard/` - Dashboard data with recommendations
- `POST /api/v1/dashboard/harvests/{planting_id}/mark-harvested` - Mark harvest complete
- `GET /api/v1/translations/{language}` - Get translations for UI
- `GET /api/v1/farms/` - Farm management
- `GET /api/v1/plantings/` - Planting management
- `GET /api/v1/harvests/` - Harvest management

## Contributing

When contributing to the system:

1. **Documentation First**: Update relevant documentation for any new features
2. **Code Comments**: Add comprehensive docstrings to new functions
3. **Translation Keys**: Add translation keys for new UI elements
4. **Testing**: Test with various scenarios and edge cases
5. **Backward Compatibility**: Consider impact on existing functionality

## Documentation Standards

### Code Documentation
- Use comprehensive docstrings for all functions
- Include type hints and return types
- Provide usage examples where helpful
- Document complex algorithms step-by-step

### API Documentation
- Document all endpoints with examples
- Include request/response schemas
- Explain error conditions and codes
- Provide usage scenarios

### User Documentation
- Write clear, concise explanations
- Include screenshots where helpful
- Provide step-by-step instructions
- Consider multiple user skill levels

## Future Documentation

Planned documentation additions:

1. **User Guide** - Step-by-step instructions for farm managers
2. **API Reference** - Complete API documentation with examples
3. **Deployment Guide** - Production deployment instructions
4. **Troubleshooting Guide** - Common issues and solutions
5. **Development Guide** - Contributing and development setup

## Support

For questions about the documentation or system:

1. Check the relevant documentation files
2. Review the code comments and docstrings
3. Test with the provided examples
4. Create an issue for missing or unclear documentation

## License

This documentation is part of the AdamEasure farm management system and follows the same license terms. 