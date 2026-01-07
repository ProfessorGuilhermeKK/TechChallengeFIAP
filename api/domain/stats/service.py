from __future__ import annotations

from api.domain.common.exceptions import DataNotAvailableError
from api.infra.storage.database import BooksDatabase


class StatsService:
    def __init__(self, db: BooksDatabase):
        self.db = db

    def _ensure_available(self) -> None:
        if not self.db.is_available():
            raise DataNotAvailableError("Data not available. Please run scraping first.")

    def get_overview(self):
        self._ensure_available()
        return self.db.get_stats_overview()

    def get_category_stats(self):
        self._ensure_available()
        return self.db.get_category_stats()
