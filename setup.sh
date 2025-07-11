#!/bin/bash

echo "🚀 Setting up Farm Management System..."

# Create necessary directories
mkdir -p backend/app/{api/endpoints,models,schemas,services,utils,core}
mkdir -p backend/alembic/versions
mkdir -p frontend/src/{components,pages,hooks,services,types,utils}

# Backend setup
echo "📦 Setting up Python backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost/farm_management
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ENVIRONMENT=development
EOF

# Initialize Alembic
alembic init alembic

# Frontend setup
echo "📦 Setting up React frontend..."
cd ../frontend

# Install dependencies
npm install

echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "1. Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Don't forget to:"
echo "- Set up PostgreSQL database"
echo "- Update DATABASE_URL in backend/.env"
echo "- Run database migrations: cd backend && alembic upgrade head" 