from fastapi import APIRouter

from app.core.config import settings

from .api_v1.api import api_router as api_v1_router
from .frontend.frontend import router as frontend_router

router = APIRouter()
router.include_router(api_v1_router, prefix=settings.API_V1_STR)
router.include_router(frontend_router, prefix="")
