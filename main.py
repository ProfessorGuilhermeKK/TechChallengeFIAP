"""
Aplicação principal da API de Livros
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from pathlib import Path

from config import get_settings
from api.routers import books, categories, stats, health, auth, ml, scraping
from api.database import get_database

# Configurar logging
from utils.logger import setup_logging
setup_logging()

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    logger.info("Starting Books API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Version: {settings.api_version}")
    
    # Criar diretórios necessários
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Carregar dados
    db = get_database(settings.data_path)
    if db.is_available():
        logger.info(f"Data loaded: {len(db.df)} books available")
    else:
        logger.warning("No data available. Please run scraping first.")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Books API...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url=f"/api/{settings.api_version}/docs",
    redoc_url=f"/api/{settings.api_version}/redoc",
    openapi_url=f"/api/{settings.api_version}/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de todas as requisições"""
    start_time = time.time()
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de processamento
    process_time = time.time() - start_time
    
    # Log
    logger.info(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Time: {process_time:.3f}s"
    )
    
    # Adicionar header com tempo de processamento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handler para 404"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handler para 500"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An internal server error occurred",
            "detail": str(exc) if settings.environment == "development" else None
        }
    )


# Rota raiz
@app.get("/", tags=["root"])
async def root():
    """Rota raiz da API"""
    return {
        "message": "Books API - Tech Challenge FIAP",
        "version": settings.api_version,
        "docs": f"/api/{settings.api_version}/docs",
        "health": f"/api/{settings.api_version}/health"
    }


# Incluir routers
api_prefix = f"/api/{settings.api_version}"

app.include_router(health.router, prefix=api_prefix)
app.include_router(books.router, prefix=api_prefix)
app.include_router(categories.router, prefix=api_prefix)
app.include_router(stats.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(ml.router, prefix=api_prefix)
app.include_router(scraping.router, prefix=api_prefix)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development"
    )



