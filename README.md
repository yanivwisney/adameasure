# Farm Management System

A comprehensive web and mobile application for managing farm operations, optimizing planting schedules, and tracking crop production.

## Features

- **Smart Planting Scheduler**: Suggests optimal planting times based on selling dates and growing conditions
- **Crop Management**: Track planting, growing, and harvesting data for each crop
- **Farm Layout Management**: Manage bed dimensions and farm layout
- **Crop Metadata Database**: Comprehensive growing information for fruits, vegetables, and other crops
- **Responsive Design**: Works seamlessly on both web and mobile devices

## Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **PostgreSQL** - Database
- **Alembic** - Database migrations

### Frontend
- **TypeScript**
- **React 18**
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **React Query** - Data fetching
- **Zustand** - State management

## Project Structure

```
farm-management/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── alembic/            # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── main.py             # Application entry point
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utilities
│   ├── package.json        # Node.js dependencies
│   └── tsconfig.json       # TypeScript config
└── docs/                   # Documentation
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Development

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

## Core Concepts

### Farm Layout
- **Beds**: Individual growing areas with defined dimensions
- **Bed Dimensions**: Length and width in meters
- **Crop Rotation**: Planning for optimal bed utilization

### Crop Metadata
- **Growing Time**: Days from planting to harvest
- **Seasonal Requirements**: Best planting seasons
- **Climate Considerations**: Temperature, humidity, sunlight needs
- **Spacing Requirements**: Distance between plants
- **Yield Estimates**: Expected production per unit area

### Planting Schedule
- **Target Selling Date**: When the farmer wants to sell
- **Selling Frequency**: How often they want to sell (every X days)
- **Crop Selection**: What to plant based on season and market demand
- **Bed Allocation**: Where to plant each crop for optimal yield

## Data Models

### Core Entities
1. **Farm**: Overall farm configuration and layout
2. **Bed**: Individual growing areas with dimensions
3. **Crop**: Crop metadata and growing information
4. **Planting**: Actual planting records with dates and locations
5. **Harvest**: Harvesting records with yields and dates
6. **Selling Schedule**: Planned selling dates and frequencies
