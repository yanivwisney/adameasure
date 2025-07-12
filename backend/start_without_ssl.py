#!/usr/bin/env python3
"""
Startup script that works around SSL issues
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_minimal_app():
    """Create a minimal FastAPI app without SSL dependencies"""

    # Create a simple FastAPI app
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="Farm Management System API",
        description="API for managing farm operations, planting schedules, and crop tracking",
        version="1.0.0",
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
        return {
            "message": "Farm Management System API",
            "version": "1.0.0",
            "status": "running",
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "message": "Backend is working!"}

    @app.get("/api/v1/features")
    async def get_features():
        return {
            "features": [
                {
                    "name": "Smart Planting Scheduler",
                    "description": "Suggests optimal planting times based on selling dates and growing conditions",
                    "status": "ready",
                },
                {
                    "name": "Crop Management",
                    "description": "Track planting, growing, and harvesting data for each crop",
                    "status": "ready",
                },
                {
                    "name": "Farm Layout Management",
                    "description": "Manage bed dimensions and farm layout",
                    "status": "ready",
                },
                {
                    "name": "Planting Tracking",
                    "description": "Record actual plantings with dates and locations",
                    "status": "ready",
                },
            ]
        }

    @app.get("/api/v1/crops/sample")
    async def get_sample_crops():
        return {
            "crops": [
                {
                    "id": 1,
                    "name": "Tomatoes",
                    "category": "vegetable",
                    "growing_time_days": 70,
                    "expected_yield_per_sqm": 8.0,
                    "market_price_per_kg": 3.5,
                },
                {
                    "id": 2,
                    "name": "Lettuce",
                    "category": "vegetable",
                    "growing_time_days": 45,
                    "expected_yield_per_sqm": 2.5,
                    "market_price_per_kg": 2.0,
                },
                {
                    "id": 3,
                    "name": "Carrots",
                    "category": "vegetable",
                    "growing_time_days": 75,
                    "expected_yield_per_sqm": 4.0,
                    "market_price_per_kg": 1.8,
                },
            ]
        }

    @app.post("/api/v1/planting-suggestions")
    async def get_planting_suggestions():
        return {
            "suggestions": [
                {
                    "crop_id": 1,
                    "crop_name": "Tomatoes",
                    "bed_id": 1,
                    "bed_name": "Bed A1",
                    "planting_date": "2024-03-15T00:00:00",
                    "expected_harvest_date": "2024-05-24T00:00:00",
                    "suggested_quantity": 24,
                    "priority": 0.85,
                },
                {
                    "crop_id": 2,
                    "crop_name": "Lettuce",
                    "bed_id": 2,
                    "bed_name": "Bed B2",
                    "planting_date": "2024-03-20T00:00:00",
                    "expected_harvest_date": "2024-05-04T00:00:00",
                    "suggested_quantity": 50,
                    "priority": 0.72,
                },
            ]
        }

    return app


def main():
    print("🚀 Starting Farm Management System Backend...")
    print("📝 Note: Running in minimal mode due to SSL library issues")
    print("🔧 To fix SSL issues, consider:")
    print("   1. Reinstalling Python with pyenv: pyenv install 3.8.7")
    print("   2. Or using system Python: /usr/bin/python3")
    print("   3. Or installing OpenSSL: brew install openssl@1.1")
    print()

    try:
        # Create the app
        app = create_minimal_app()

        print("✅ App created successfully!")
        print("🌐 Starting server on http://localhost:8000")
        print("📚 API documentation at http://localhost:8000/docs")
        print("🏥 Health check at http://localhost:8000/health")
        print("📋 Features at http://localhost:8000/api/v1/features")
        print("🌱 Sample crops at http://localhost:8000/api/v1/crops/sample")
        print()
        print("Press Ctrl+C to stop the server")
        print()

        # Start the server
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing dependencies with: pip3 install fastapi uvicorn")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 This might be due to SSL library issues.")


if __name__ == "__main__":
    main()
