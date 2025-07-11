from fastapi import APIRouter
from app.api.endpoints import farms, beds, crops, plantings, selling_schedules
from app.api import harvests

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(farms.router, prefix="/farms", tags=["farms"])
api_router.include_router(beds.router, prefix="/beds", tags=["beds"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(plantings.router, prefix="/plantings", tags=["plantings"])
api_router.include_router(selling_schedules.router, prefix="/selling-schedules", tags=["selling-schedules"])
api_router.include_router(harvests.router, prefix="/harvests", tags=["harvests"]) 