import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


class BooksDatabase:
    def __init__(self, data_path: str = "data/books.csv"):
        self.data_path = Path(data_path)
        self._df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _load_data(self):
        try:
            if self.data_path.exists():
                self._df = pd.read_csv(self.data_path)
                logger.info(f"Dados carregados com sucesso: {len(self._df)} livros")
            else:
                logger.warning(f"Arquivo de dados não encontrado: {self.data_path}")
                self._df = pd.DataFrame()
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            self._df = pd.DataFrame()
    
    def reload_data(self):
        self._load_data()
    
    @property
    def df(self) -> pd.DataFrame:
        if self._df is None or self._df.empty:
            self._load_data()
        return self._df
    
    @property
    def total_books(self) -> int:
        if not self.is_available():
            return 0
        return len(self._df)
    
    def is_available(self) -> bool:
        return self._df is not None and not self._df.empty
    
    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        if not self.is_available():
            return []
        
        df_paginated = self.df.iloc[skip:skip + limit]
        return df_paginated.to_dict('records')
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        if not self.is_available():
            return None
        
        book = self.df[self.df['id'] == book_id]
        if book.empty:
            return None
        
        return book.iloc[0].to_dict()
    
    def search_books(
        self,
        title: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[int] = None,
        in_stock: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        if not self.is_available():
            return []
        
        df_filtered = self.df.copy()
        
        if title:
            df_filtered = df_filtered[
                df_filtered['title'].str.contains(title, case=False, na=False)
            ]
        
        if category:
            df_filtered = df_filtered[
                df_filtered['category'].str.contains(category, case=False, na=False)
            ]
        
        if min_price is not None:
            df_filtered = df_filtered[df_filtered['price'] >= min_price]
        
        if max_price is not None:
            df_filtered = df_filtered[df_filtered['price'] <= max_price]
        
        if min_rating is not None:
            df_filtered = df_filtered[df_filtered['rating'] >= min_rating]
        
        if in_stock is not None:
            df_filtered = df_filtered[df_filtered['in_stock'] == in_stock]
        
        df_paginated = df_filtered.iloc[skip:skip + limit]
        return df_paginated.to_dict('records')
    
    def get_all_categories(self) -> List[Dict[str, any]]:
        if not self.is_available():
            return []
        
        categories = self.df.groupby('category').size().reset_index(name='total_books')
        return categories.to_dict('records')
    
    def get_top_rated_books(self, limit: int = 10) -> List[Dict]:
        if not self.is_available():
            return []
        
        df_sorted = self.df.sort_values(['rating', 'title'], ascending=[False, True])
        return df_sorted.head(limit).to_dict('records')
    
    def get_books_by_price_range(
        self,
        min_price: float,
        max_price: float,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        if not self.is_available():
            return []
        
        df_filtered = self.df[
            (self.df['price'] >= min_price) & (self.df['price'] <= max_price)
        ]
        
        df_paginated = df_filtered.iloc[skip:skip + limit]
        return df_paginated.to_dict('records')
    
    def get_stats_overview(self) -> Dict[str, any]:
        if not self.is_available():
            return {}
        
        rating_dist = self.df['rating'].value_counts().to_dict()
        rating_distribution = {str(k): int(v) for k, v in rating_dist.items()}
        
        stats = {
            'total_books': int(len(self.df)),
            'total_categories': int(self.df['category'].nunique()),
            'average_price': float(self.df['price'].mean()),
            'min_price': float(self.df['price'].min()),
            'max_price': float(self.df['price'].max()),
            'average_rating': float(self.df['rating'].mean()),
            'books_in_stock': int(self.df['in_stock'].sum()),
            'books_out_of_stock': int((~self.df['in_stock']).sum()),
            'rating_distribution': rating_distribution
        }
        
        return stats
    
    def get_category_stats(self) -> List[Dict[str, any]]:
        if not self.is_available():
            return []
        
        stats_list = []
        
        for category in self.df['category'].unique():
            df_cat = self.df[self.df['category'] == category]
            
            stats = {
                'category': category,
                'total_books': int(len(df_cat)),
                'average_price': float(df_cat['price'].mean()),
                'min_price': float(df_cat['price'].min()),
                'max_price': float(df_cat['price'].max()),
                'average_rating': float(df_cat['rating'].mean()),
                'books_in_stock': int(df_cat['in_stock'].sum())
            }
            
            stats_list.append(stats)
        
        stats_list.sort(key=lambda x: x['total_books'], reverse=True)
        
        return stats_list
    
    def get_ml_features(self) -> List[Dict[str, any]]:
        if not self.is_available():
            return []
        
        df_ml = self.df.copy()
        
        price_min = df_ml['price'].min()
        price_max = df_ml['price'].max()
        df_ml['price_normalized'] = (df_ml['price'] - price_min) / (price_max - price_min)
        
        df_ml['rating_normalized'] = df_ml['rating'] / 5.0
        
        categories = df_ml['category'].unique()
        category_map = {cat: idx for idx, cat in enumerate(categories)}
        df_ml['category_encoded'] = df_ml['category'].map(category_map)
        
        features = df_ml[[
            'id', 'title', 'price', 'rating', 'category',
            'in_stock', 'price_normalized', 'rating_normalized', 'category_encoded'
        ]]
        
        return features.to_dict('records')


_db_instance: Optional[BooksDatabase] = None


def get_database(data_path: str = "data/books.csv") -> BooksDatabase:
    global _db_instance
    if _db_instance is None:
        _db_instance = BooksDatabase(data_path)
    return _db_instance





