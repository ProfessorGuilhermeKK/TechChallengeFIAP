from fastapi import APIRouter, Depends
from typing import List
import logging

from api.core.deps import get_stats_service
from api.domain.stats.schemas import CategoryStats, StatsOverview
from api.domain.stats.service import StatsService

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
async def get_stats_overview(
    service: StatsService = Depends(get_stats_service),
):
    return service.get_overview()


@router.get(
    "/categories",
    response_model=List[CategoryStats],
    summary="Estatísticas por categoria",
    description="Retorna estatísticas detalhadas de cada categoria"
)
async def get_category_stats(
    service: StatsService = Depends(get_stats_service),
):
    return service.get_category_stats()
