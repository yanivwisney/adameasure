#!/bin/bash

echo "🚀 Quick Setup for Farm Management System"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "📦 Installing Python dependencies..."

# Install dependencies
cd backend
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the error above."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost/farm_management
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ENVIRONMENT=development
EOF
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the backend server:"
echo "  cd backend && python3 start.py"
echo ""
echo "Or manually:"
echo "  cd backend && uvicorn main:app --reload"
echo ""
echo "📚 API documentation will be available at: http://localhost:8000/docs"
echo ""
echo "⚠️  Note: You'll need to set up PostgreSQL database and update DATABASE_URL in .env" 