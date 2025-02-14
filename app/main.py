from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.core.middleware import (
    RequestIDMiddleware,
    ResponseTimeMiddleware,
    RateLimitMiddleware
)

# Setup logging
logger = setup_logging()

app = FastAPI(
    title="Kryos API",
    description="Enterprise-grade cryptocurrency intelligence platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(ResponseTimeMiddleware)
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "http_error"
            }
        }
    )

def custom_openapi():
    """Customize OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Kryos API",
        version="0.1.0",
        description="Enterprise-grade cryptocurrency intelligence platform",
        routes=app.routes,
    )

    # Custom OpenAPI schema modifications
    openapi_schema["info"]["x-logo"] = {
        "url": "https://kryos.ai/logo.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi 
