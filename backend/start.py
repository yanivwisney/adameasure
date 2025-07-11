#!/usr/bin/env python3
"""
Simple startup script for the Farm Management System backend
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""DATABASE_URL=postgresql://user:password@localhost/farm_management
SECRET_KEY=your-secret-key-change-this-in-production
DEBUG=True
ENVIRONMENT=development
""")
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Starting Farm Management System Backend...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("🌐 Starting server on http://localhost:8000")
    print("📚 API documentation available at http://localhost:8000/docs")
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main() 