"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, intake, users, dashboard, agents, work_orders, artifacts

# Import all models to register them with SQLAlchemy
# This ensures foreign key relationships can be resolved at runtime
from app.models import (
    Tenant, User, FileUpload, Dataset, MappingConfig,
    PolicyPack, WorkOrder, AuditEvent, Artifact
)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Production-ready full-stack application API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
# Allow requests from frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Explicit origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api")
app.include_router(intake.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(work_orders.router, prefix="/api")
app.include_router(artifacts.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name
    }


@app.get("/api/test-cors")
async def test_cors():
    """Test CORS configuration."""
    return {
        "message": "CORS is working!",
        "cors_enabled": True
    }
