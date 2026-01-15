from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    api_version: str = "v1"
    api_title: str = "Books API - Tech Challenge"
    api_description: str = "API pública para consulta de livros extraídos via web scraping"
    host: str = "127.0.0.1"
    port: int = 8000
    
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    auth_users: str = "admin:secret:Admin User:admin@booksapi.com,testuser:secret:Test User:test@booksapi.com"
    
    data_path: str = "data/books.csv"
    scraping_url: str = "https://books.toscrape.com"
    
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

