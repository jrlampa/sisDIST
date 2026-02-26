"""Main API router aggregating all versioned sub-routers."""
from fastapi import APIRouter
from app.api.v1 import mapping, infrastructure, calculations, projects

api_router = APIRouter()

api_router.include_router(mapping.router, prefix="/v1/mapping", tags=["mapping"])
api_router.include_router(infrastructure.router, prefix="/v1/infrastructure", tags=["infrastructure"])
api_router.include_router(calculations.router, prefix="/v1/calculations", tags=["calculations"])
api_router.include_router(projects.router, prefix="/v1/projects", tags=["projects"])
