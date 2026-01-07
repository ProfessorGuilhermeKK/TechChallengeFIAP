"""
Endpoint de health check
"""
from fastapi import APIRouter
from datetime import datetime
from api.domain.common.health_schemas import HealthCheck
from api.infra.storage.database import get_database
from api.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(
    tags=["health"],
)


@router.get(
    "/health",
    response_model=HealthCheck,
    summary="Health Check",
    description="Verifica o status da API e a disponibilidade dos dados"
)
async def health_check():
    """Verifica o status da API"""
    db = get_database()
    
    data_available = db.is_available()
    total_books = len(db.df) if data_available else 0
    
    status = "healthy" if data_available else "degraded"
    message = None if data_available else "Data not available. Please run scraping first."
    
    return {
        "status": status,
        "version": settings.api_version,
        "timestamp": datetime.utcnow(),
        "data_available": data_available,
        "total_books": total_books,
        "message": message
    }





