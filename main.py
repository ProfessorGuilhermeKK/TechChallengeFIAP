import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from pathlib import Path

from prometheus_fastapi_instrumentator import Instrumentator

from api.core.config import get_settings
from api.core.exception_handlers import register_exception_handlers
from api.routers import books, categories, stats, health, auth, ml, scraping
from api.infra.storage.database import get_database
from api.core.logger import setup_logging, request_id_var, user_var
setup_logging()

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Books API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Version: {settings.api_version}")
    
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    db = get_database(settings.data_path)
    if db.is_available():
        logger.info(f"Data loaded: {len(db.df)} books available")
    else:
        logger.warning("No data available. Please run scraping first.")
    
    yield
    
    logger.info("Shutting down Books API...")


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url=f"/api/{settings.api_version}/docs",
    redoc_url=f"/api/{settings.api_version}/redoc",
    openapi_url=f"/api/{settings.api_version}/openapi.json",
)

register_exception_handlers(app)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request_id_token = request_id_var.set(request_id)
    user_token = user_var.set(None)

    start = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000

        logger.exception(
            "request_failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration_ms, 2),
            },
        )
        raise
    finally:
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "user": user_var.get(),
            },
        )
        
        user_var.reset(user_token)
        request_id_var.reset(request_id_token)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration_ms / 1000:.3f}"

    return response


@app.get("/", tags=["root"])
async def root():
    dashboard_url = "https://seu-dashboard.streamlit.app"
    
    return {
        "message": "Books API - Tech Challenge FIAP",
        "version": settings.api_version,
        "docs": f"/api/{settings.api_version}/docs",
        "health": f"/api/{settings.api_version}/health",
        "dashboard": dashboard_url,
        "note": "Acesse o dashboard em: " + dashboard_url
    }


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





