#!/usr/bin/env python3
"""
Simple test script to verify the backend works without SSL dependencies
"""

def test_imports():
    """Test if we can import the basic modules"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import pydantic
        print("✅ Pydantic imported successfully")
        
        # Test our app imports
        from app.core.config import settings
        print("✅ App config imported successfully")
        
        from app.core.database import get_db
        print("✅ Database module imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_simple_app():
    """Create a simple FastAPI app for testing"""
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(
            title="Farm Management System API",
            description="API for managing farm operations",
            version="1.0.0"
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/")
        async def root():
            return {"message": "Farm Management System API", "status": "running"}
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "message": "Backend is working!"}
        
        @app.get("/test")
        async def test():
            return {
                "message": "Test endpoint working!",
                "features": [
                    "Smart Planting Scheduler",
                    "Crop Management", 
                    "Farm Layout Management",
                    "Planting Tracking"
                ]
            }
        
        return app
        
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return None

def main():
    print("🧪 Testing Farm Management System Backend...")
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed. Please check your Python environment.")
        return
    
    # Create simple app
    app = create_simple_app()
    if not app:
        print("❌ Failed to create app.")
        return
    
    print("\n🚀 Starting simple test server...")
    print("📚 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    print("🏥 Health check at: http://localhost:8000/health")
    print("🧪 Test endpoint at: http://localhost:8000/test")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main() 