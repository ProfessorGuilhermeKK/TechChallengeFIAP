"""
Endpoint para trigger de scraping (protegido por autenticação)
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from api.core.auth import get_current_active_user
import logging

from api.core.deps import get_scraping_service
from api.domain.auth.schemas import User
from api.domain.scraping.service import ScrapingService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/trigger",
    summary="Trigger Scraping",
    description="Inicia processo de scraping do site (requer autenticação)"
)
async def trigger_scraping(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    service: ScrapingService = Depends(get_scraping_service),
):
    logger.info(f"Scraping triggered by user: {current_user.username}")

    service.trigger_scraping(background_tasks)

    return {
        "status": "success",
        "message": "Scraping task started in background",
        "triggered_by": current_user.username
    }


@router.post(
    "/reload",
    summary="Reload Data",
    description="Recarrega dados do CSV sem executar scraping (requer autenticação)"
)
async def reload_data(
    service: ScrapingService = Depends(get_scraping_service),
):
    total = service.reload_data()
    return {
        "status": "success",
        "message": "Data reloaded successfully",
        "total_books": total
    }
