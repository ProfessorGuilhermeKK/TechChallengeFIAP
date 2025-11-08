"""
Endpoints relacionados a livros
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
from api.models import Book, BookList
from api.database import get_database
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    response_model=BookList,
    summary="Lista todos os livros",
    description="Retorna uma lista paginada de todos os livros disponíveis na base de dados"
)
async def get_all_books(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamanho da página")
):
    """Lista todos os livros com paginação"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    skip = (page - 1) * page_size
    books = db.get_all_books(skip=skip, limit=page_size)
    total = len(db.df)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "books": books
    }


@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Obtém detalhes de um livro",
    description="Retorna informações detalhadas de um livro específico pelo ID"
)
async def get_book_by_id(
    book_id: int = Path(..., ge=1, description="ID do livro")
):
    """Retorna detalhes de um livro específico"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    book = db.get_book_by_id(book_id)
    
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with ID {book_id} not found"
        )
    
    return book


@router.get(
    "/search/query",
    response_model=BookList,
    summary="Busca livros",
    description="Busca livros por título e/ou categoria com paginação"
)
async def search_books(
    title: Optional[str] = Query(None, description="Filtro por título (busca parcial)"),
    category: Optional[str] = Query(None, description="Filtro por categoria"),
    min_price: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    min_rating: Optional[int] = Query(None, ge=0, le=5, description="Rating mínimo"),
    in_stock: Optional[bool] = Query(None, description="Filtro por disponibilidade"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamanho da página")
):
    """Busca livros com múltiplos filtros"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    skip = (page - 1) * page_size
    
    books = db.search_books(
        title=title,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock=in_stock,
        skip=skip,
        limit=page_size
    )
    
    # Contar total de resultados (sem paginação)
    all_results = db.search_books(
        title=title,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock=in_stock,
        skip=0,
        limit=999999
    )
    
    return {
        "total": len(all_results),
        "page": page,
        "page_size": page_size,
        "books": books
    }


@router.get(
    "/top-rated/list",
    response_model=List[Book],
    summary="Livros mais bem avaliados",
    description="Lista os livros com melhor avaliação (rating mais alto)"
)
async def get_top_rated_books(
    limit: int = Query(10, ge=1, le=100, description="Número de livros a retornar")
):
    """Retorna os livros com melhor avaliação"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    books = db.get_top_rated_books(limit=limit)
    return books


@router.get(
    "/price-range/filter",
    response_model=BookList,
    summary="Filtra livros por faixa de preço",
    description="Retorna livros dentro de uma faixa de preço específica"
)
async def get_books_by_price_range(
    min: float = Query(..., ge=0, description="Preço mínimo"),
    max: float = Query(..., ge=0, description="Preço máximo"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamanho da página")
):
    """Filtra livros por faixa de preço"""
    db = get_database()
    
    if not db.is_available():
        raise HTTPException(
            status_code=503,
            detail="Data not available. Please run scraping first."
        )
    
    if min > max:
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot be greater than maximum price"
        )
    
    skip = (page - 1) * page_size
    books = db.get_books_by_price_range(min, max, skip=skip, limit=page_size)
    
    # Contar total
    all_books = db.get_books_by_price_range(min, max, skip=0, limit=999999)
    
    return {
        "total": len(all_books),
        "page": page,
        "page_size": page_size,
        "books": books
    }





