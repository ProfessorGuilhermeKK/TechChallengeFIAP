#!/usr/bin/env python3
import uvicorn
from api.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print("=" * 60)
    print("Books API - Tech Challenge FIAP")
    print("=" * 60)
    print(f"Environment: {settings.environment}")
    print(f"API Version: {settings.api_version}")
    print(f"Host: {settings.host}:{settings.port}")
    print(f"Docs: http://{settings.host}:{settings.port}/api/{settings.api_version}/docs")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level="info"
    )





