from __future__ import annotations

from typing import Any, Dict, List, Optional

from api.domain.common.exceptions import DataNotAvailableError, InvalidInputError, NotFoundError
from api.infra.storage.database import BooksDatabase


class BooksService:
    """
    Service (regra de negócio).

    Aqui fica:
    - validações
    - paginação
    - "montagem" de resposta (total/page/page_size/books)
    """

    def __init__(self, db: BooksDatabase):
        self.db = db

    def _ensure_available(self) -> None:
        if not self.db.is_available():
            raise DataNotAvailableError("Data not available. Please run scraping first.")

    def get_all_books(self, page: int, page_size: int) -> Dict[str, Any]:
        self._ensure_available()

        skip = (page - 1) * page_size
        books = self.db.get_all_books(skip=skip, limit=page_size)

        return {
            "total": self.db.total_books,
            "page": page,
            "page_size": page_size,
            "books": books,
        }

    def get_book_by_id(self, book_id: int) -> Dict[str, Any]:
        self._ensure_available()

        book = self.db.get_book_by_id(book_id)
        if not book:
            raise NotFoundError(f"Book with ID {book_id} not found")

        return book

    def search_books(
        self,
        title: Optional[str],
        category: Optional[str],
        min_price: Optional[float],
        max_price: Optional[float],
        min_rating: Optional[int],
        in_stock: Optional[bool],
        page: int,
        page_size: int,
    ) -> Dict[str, Any]:
        self._ensure_available()

        skip = (page - 1) * page_size

        books = self.db.search_books(
            title=title,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            in_stock=in_stock,
            skip=skip,
            limit=page_size,
        )

        # Mantendo o comportamento atual do router:
        # ele calcula o total rodando a busca "sem paginação" com limit gigante. :contentReference[oaicite:1]{index=1}
        all_results = self.db.search_books(
            title=title,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            in_stock=in_stock,
            skip=0,
            limit=999999,
        )

        return {
            "total": len(all_results),
            "page": page,
            "page_size": page_size,
            "books": books,
        }

    def get_top_rated_books(self, limit: int) -> List[Dict[str, Any]]:
        self._ensure_available()
        return self.db.get_top_rated_books(limit=limit)

    def get_books_by_price_range(
        self, min_price: float, max_price: float, page: int, page_size: int
    ) -> Dict[str, Any]:
        self._ensure_available()

        if min_price > max_price:
            raise InvalidInputError("Minimum price cannot be greater than maximum price")

        skip = (page - 1) * page_size
        books = self.db.get_books_by_price_range(
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=page_size,
        )

        # Mantendo o comportamento atual do router (total com limit gigante). :contentReference[oaicite:2]{index=2}
        all_books = self.db.get_books_by_price_range(
            min_price=min_price,
            max_price=max_price,
            skip=0,
            limit=999999,
        )

        return {
            "total": len(all_books),
            "page": page,
            "page_size": page_size,
            "books": books,
        }
