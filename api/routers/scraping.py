"""
Endpoint para trigger de scraping (protegido por autenticação)
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from api.models import User
from api.auth import get_current_active_user
from api.database import get_database
from scripts.scraper import BooksScraper
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scraping",
    tags=["scraping"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)


def run_scraping_task():
    """Executa o scraping em background"""
    try:
        logger.info("Starting scraping task...")
        scraper = BooksScraper()
        df_books = scraper.scrape_all_books()
        scraper.save_to_csv(df_books, 'data/books.csv')
        
        # Recarregar dados no banco
        db = get_database()
        db.reload_data()
        
        logger.info("Scraping task completed successfully")
    except Exception as e:
        logger.error(f"Error in scraping task: {e}")


@router.post(
    "/trigger",
    summary="Trigger Scraping",
    description="Inicia processo de scraping do site (requer autenticação)"
)
async def trigger_scraping(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user)
):
    """
    Inicia o processo de scraping em background
    
    Este endpoint requer autenticação JWT.
    """
    logger.info(f"Scraping triggered by user: {current_user.username}")
    
    background_tasks.add_task(run_scraping_task)
    
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
async def reload_data(current_user: User = Depends(get_current_active_user)):
    """Recarrega os dados do CSV"""
    try:
        db = get_database()
        db.reload_data()
        
        return {
            "status": "success",
            "message": "Data reloaded successfully",
            "total_books": len(db.df)
        }
    except Exception as e:
        logger.error(f"Error reloading data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error reloading data: {str(e)}"
        )





