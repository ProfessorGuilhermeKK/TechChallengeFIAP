"""
Configurações centralizadas da aplicação
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API Configuration
    api_version: str = "v1"
    api_title: str = "Books API - Tech Challenge"
    api_description: str = "API pública para consulta de livros extraídos via web scraping"
    host: str = "127.0.0.1"  # Use "0.0.0.0" para produção/deploy
    port: int = 8000
    
    # JWT Authentication
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Authentication Users
    # Formato: username:password:fullname:email,username2:password2:fullname2:email2
    # Exemplo: admin:secret:Admin User:admin@example.com,user:pass:User Name:user@example.com
    auth_users: str = "admin:secret:Admin User:admin@booksapi.com,testuser:secret:Test User:test@booksapi.com"
    
    # Data Configuration
    data_path: str = "data/books.csv"
    scraping_url: str = "https://books.toscrape.com"
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Não falhar se .env não existir
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância singleton das configurações"""
    return Settings()

