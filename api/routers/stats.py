"""
Endpoints de estatísticas e insights
"""
from fastapi import APIRouter, HTTPException
from typing import List
from api.models import StatsOverview, CategoryStats
from api.database import get_database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/stats",
    tags=["statistics"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/overview",
    response_model=StatsOverview,
    summary="Estatísticas gerais",
    description="Retorna estatísticas gerais da coleção de livros"
)
async def get_stats_overview():
    """Retorna estatísticas gerais da coleção"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    stats = db.get_stats_overview()
    return stats


@router.get(
    "/categories",
    response_model=List[CategoryStats],
    summary="Estatísticas por categoria",
    description="Retorna estatísticas detalhadas de cada categoria"
)
async def get_category_stats():
    """Retorna estatísticas detalhadas por categoria"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    stats = db.get_category_stats()
    return stats





