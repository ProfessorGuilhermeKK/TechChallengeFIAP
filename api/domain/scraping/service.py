from __future__ import annotations

import logging
from fastapi import BackgroundTasks

from api.infra.scraping.scraper import BooksScraper
from api.infra.storage.database import BooksDatabase

logger = logging.getLogger(__name__)


class ScrapingService:
    def __init__(self, db: BooksDatabase):
        self.db = db

    def _run_scraping_task(self) -> None:
        logger.info("Starting scraping task...")
        scraper = BooksScraper()

        df_books = scraper.scrape_all_books()
        scraper.save_to_csv(df_books, "data/books.csv")

        self.db.reload_data()

        logger.info("Scraping task completed successfully")

    def trigger_scraping(self, background_tasks: BackgroundTasks) -> None:
        background_tasks.add_task(self._run_scraping_task)

    def reload_data(self) -> int:
        self.db.reload_data()
        return len(self.db.df)
