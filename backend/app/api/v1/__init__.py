"""API v1 router configuration"""

from fastapi import APIRouter
from app.api.v1.endpoints import algorithms, categories, languages, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["algorithms"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(languages.router, prefix="/languages", tags=["languages"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include admin routers
api_router.include_router(algorithms.admin_router, prefix="/admin/algorithms", tags=["algorithms"])
