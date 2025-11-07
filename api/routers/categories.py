"""
Endpoints relacionados a categorias
"""
from fastapi import APIRouter, HTTPException
from api.models import CategoryList
from api.database import get_database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=CategoryList,
    summary="Lista todas as categorias",
    description="Retorna lista de todas as categorias de livros disponíveis com contagem"
)
async def get_all_categories():
    """Lista todas as categorias de livros"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    categories = db.get_all_categories()
    
    return {
        "total": len(categories),
        "categories": [
            {"name": cat["category"], "total_books": cat["total_books"]}
            for cat in categories
        ]
    }



