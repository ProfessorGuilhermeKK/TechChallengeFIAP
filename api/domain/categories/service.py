from __future__ import annotations

from typing import Any, Dict

from api.domain.common.exceptions import DataNotAvailableError
from api.infra.storage.database import BooksDatabase


class CategoriesService:
    def __init__(self, db: BooksDatabase):
        self.db = db

    def _ensure_available(self) -> None:
        if not self.db.is_available():
            raise DataNotAvailableError("Data not available. Please run scraping first.")

    def list_categories(self) -> Dict[str, Any]:
        self._ensure_available()

        categories = self.db.get_all_categories()

        return {
            "total": len(categories),
            "categories": [
                {"name": cat["category"], "total_books": cat["total_books"]}
                for cat in categories
            ],
        }
