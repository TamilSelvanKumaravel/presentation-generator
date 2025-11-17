"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import presentation
from src.config.settings import settings
from src.utils.logger import setup_logger, app_logger

# Setup logger
setup_logger(settings.log_level)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered presentation generator using LLMs"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(presentation.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Presentation Generator API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    app_logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    app_logger.info(f"LLM Provider: {settings.llm_provider}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    app_logger.info("Shutting down application")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

