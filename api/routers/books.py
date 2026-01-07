"""
Endpoints relacionados a livros
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Optional, List

from api.core.deps import get_books_service
from api.domain.books.schemas import Book, BookList
from api.domain.books.service import BooksService
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
    description="Retorna uma lista paginada de todos os livros disponíveis na base de dados",
)
async def get_all_books(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamanho da página"),
    service: BooksService = Depends(get_books_service),
):
    return service.get_all_books(page=page, page_size=page_size)


@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Obtém detalhes de um livro",
    description="Retorna informações detalhadas de um livro específico pelo ID",
)
async def get_book_by_id(
    book_id: int = Path(..., ge=1, description="ID do livro"),
    service: BooksService = Depends(get_books_service),
):
    return service.get_book_by_id(book_id=book_id)


@router.get(
    "/search",
    response_model=BookList,
    summary="Busca livros",
    description="Busca livros por título e/ou categoria com paginação",
)
async def search_books(
    title: Optional[str] = Query(None, description="Filtro por título (busca parcial)"),
    category: Optional[str] = Query(None, description="Filtro por categoria"),
    min_price: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Preço máximo"),
    min_rating: Optional[int] = Query(None, ge=0, le=5, description="Rating mínimo"),
    in_stock: Optional[bool] = Query(None, description="Filtro por disponibilidade"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamanho da página"),
    service: BooksService = Depends(get_books_service),
):
    return service.search_books(
        title=title,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        in_stock=in_stock,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/top-rated",
    response_model=List[Book],
    summary="Livros mais bem avaliados",
    description="Lista os livros com melhor avaliação (rating mais alto)",
)
async def get_top_rated_books(
    limit: int = Query(10, ge=1, le=100, description="Número de livros a retornar"),
    service: BooksService = Depends(get_books_service),
):
    return service.get_top_rated_books(limit=limit)


@router.get(
    "/price-range",
    response_model=BookList,
    summary="Filtra livros por faixa de preço",
    description="Retorna livros dentro de uma faixa de preço específica",
)
async def get_books_by_price_range(
    min: float = Query(..., ge=0, description="Preço mínimo"),
    max: float = Query(..., ge=0, description="Preço máximo"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamanho da página"),
    service: BooksService = Depends(get_books_service),
):
    return service.get_books_by_price_range(
        min_price=min,
        max_price=max,
        page=page,
        page_size=page_size,
    )
