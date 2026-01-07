from __future__ import annotations

from typing import Any, Dict

from api.domain.common.exceptions import DataNotAvailableError
from api.infra.storage.database import BooksDatabase
import logging

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self, db: BooksDatabase):
        self.db = db

    def _ensure_available(self) -> None:
        if not self.db.is_available():
            raise DataNotAvailableError("Data not available. Please run scraping first.")

    def get_features(self):
        self._ensure_available()
        return self.db.get_ml_features()

    def get_training_data(self) -> Dict[str, Any]:
        self._ensure_available()

        features = self.db.get_ml_features()
        stats = self.db.get_stats_overview()

        metadata = {
            "total_samples": len(features),
            "total_categories": stats.get("total_categories", 0),
            "feature_columns": [
                "price_normalized",
                "rating_normalized",
                "category_encoded",
                "in_stock",
            ],
            "description": "Dataset de livros para treinamento de modelos de recomendação",
        }

        return {
            "features": features,
            "metadata": metadata,
        }

    def submit_predictions(self, predictions):
        # Mesmo comportamento do router atual: loga e devolve o payload recebido. :contentReference[oaicite:2]{index=2}
        logger.info(f"Received {len(predictions)} predictions")
        return predictions

    def get_ml_stats(self) -> Dict[str, Any]:
        self._ensure_available()

        stats = self.db.get_stats_overview()
        categories = self.db.get_all_categories()

        df = self.db.df
        price_quartiles = df["price"].quantile([0.25, 0.5, 0.75]).to_dict()

        total_books = stats.get("total_books", 0) or 0
        in_stock = stats.get("books_in_stock", 0) or 0
        denom = stats.get("total_books", 1) or 1  # igual ao router atual (evita div/0). :contentReference[oaicite:3]{index=3}

        return {
            "dataset_size": total_books,
            "num_categories": len(categories),
            "price_distribution": {
                "min": stats.get("min_price", 0),
                "q1": price_quartiles.get(0.25, 0),
                "median": price_quartiles.get(0.5, 0),
                "q3": price_quartiles.get(0.75, 0),
                "max": stats.get("max_price", 0),
                "mean": stats.get("average_price", 0),
            },
            "rating_distribution": stats.get("rating_distribution", {}),
            "stock_balance": {
                "in_stock": in_stock,
                "out_of_stock": stats.get("books_out_of_stock", 0),
                "in_stock_percentage": round((in_stock / denom) * 100, 2),
            },
            "category_distribution": [
                {"category": cat["category"], "count": cat["total_books"]}
                for cat in categories
            ],
        }
