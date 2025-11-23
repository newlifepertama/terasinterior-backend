from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routers import auth, portfolio, contact, service, setting, stats
from app.middleware.validation import RequestSizeLimitMiddleware
from app.middleware.rate_limit import limiter, rate_limit_handler
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from pathlib import Path

# Create FastAPI app
app = FastAPI(
    title="Teras Interior API",
    description="Backend API for Teras Interior website",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Create uploads directory if not exists
Path("uploads/portfolio").mkdir(parents=True, exist_ok=True)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# Request size limit middleware
app.add_middleware(RequestSizeLimitMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, settings.production_url],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include routers
app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(contact.router)
app.include_router(service.router)
app.include_router(setting.router)
app.include_router(stats.router)

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Teras Interior API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }
