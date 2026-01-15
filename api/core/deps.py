from fastapi import Depends

from api.domain.auth.service import AuthService
from api.domain.books.service import BooksService
from api.domain.categories.service import CategoriesService
from api.domain.ml.service import MLService
from api.domain.scraping.service import ScrapingService
from api.domain.stats.service import StatsService
from api.infra.storage.database import BooksDatabase, get_database


def get_books_database() -> BooksDatabase:
    return get_database()


def get_books_service(
    repo: BooksDatabase = Depends(get_books_database),
) -> BooksService:
    return BooksService(repo)


def get_stats_service(
    db: BooksDatabase = Depends(get_books_database),
) -> StatsService:
    return StatsService(db)


def get_ml_service(
    db: BooksDatabase = Depends(get_books_database),
) -> MLService:
    return MLService(db)


def get_scraping_service(
    db: BooksDatabase = Depends(get_books_database),
) -> ScrapingService:
    return ScrapingService(db)


def get_auth_service() -> AuthService:
    return AuthService()


def get_categories_service(
    db: BooksDatabase = Depends(get_books_database),
) -> CategoriesService:
    return CategoriesService(db)