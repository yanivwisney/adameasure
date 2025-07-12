from fastapi import APIRouter
from app.api.endpoints import (
    farms,
    crops,
    plantings,
    selling_schedules,
    translations,
    lines,
    dashboard,
)
from app.api import harvests

api_router = APIRouter()

api_router.include_router(farms.router, prefix="/farms", tags=["farms"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(plantings.router, prefix="/plantings", tags=["plantings"])
api_router.include_router(
    selling_schedules.router, prefix="/selling-schedules", tags=["selling-schedules"]
)
api_router.include_router(
    translations.router, prefix="/translations", tags=["translations"]
)
api_router.include_router(lines.router, prefix="/lines", tags=["lines"])
api_router.include_router(harvests.router, tags=["harvests"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
