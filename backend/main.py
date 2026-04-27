import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.api import auth_router, admin_router, deliver_router, member_router, older_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Elderly Food Delivery System API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
voices_dir = os.path.join(static_dir, "voices")
uploads_dir = os.path.join(static_dir, "uploads")
images_dir = os.path.join(uploads_dir, "images")
exception_images_dir = os.path.join(uploads_dir, "exception_images")
os.makedirs(voices_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)
os.makedirs(exception_images_dir, exist_ok=True)

# Mount static files directory for serving static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Register routers with API v1 prefix
app.include_router(auth_router, prefix="/api/v1")
app.include_router(older_router, prefix="/api/v1")
app.include_router(member_router, prefix="/api/v1")
app.include_router(deliver_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root path"""
    return {
        "message": "Elderly Food Delivery System API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Elderly Food Delivery System API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=7678, help="Port to bind to")
    args = parser.parse_args()
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=True
    )