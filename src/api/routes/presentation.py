"""API routes for presentation generation."""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from src.models.schemas import PresentationRequest, PresentationResponse
from src.services.llm.openai_service import OpenAIService
from src.services.llm.ollama_service import OllamaService
from src.services.presentation.pptx_generator import PPTXGenerator
from src.config.settings import settings
from src.utils.logger import app_logger
import os
from src.services.llm.openrouter_service import OpenRouterService

router = APIRouter(prefix="/presentation", tags=["presentation"])

# Initialize services
_llm_service = None
_pptx_generator = PPTXGenerator()


def get_llm_service():
    """Get LLM service based on configuration."""
    global _llm_service
    if _llm_service is None:
        if settings.llm_provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            _llm_service = OpenAIService(
                api_key=settings.openai_api_key,
                model=settings.openai_model
            )
        elif settings.llm_provider == "openrouter":
            if not settings.openai_api_key:
                raise ValueError("OpenRouter API key not configured")
            _llm_service = OpenRouterService(
                api_key=settings.openai_api_key,
                model=settings.openrouter_model
            )
        else:
            _llm_service = OllamaService(
                base_url=settings.ollama_base_url,
                model=settings.ollama_model
            )
    return _llm_service


@router.post("/generate", response_model=PresentationResponse)
async def generate_presentation(
    request: PresentationRequest,
    llm_service=Depends(get_llm_service)
):
    """Generate presentation from topic."""
    try:
        app_logger.info(f"Received presentation request: {request.topic}")
        
        # Generate content using LLM
        llm_response = await llm_service.generate_presentation_content(
            topic=request.topic,
            number_of_slides=request.number_of_slides,
            style=request.style,
            language=request.language,
            include_images=request.include_images
        )
        
        # Generate presentation file
        if request.format == "pptx":
            file_path = _pptx_generator.generate(llm_response, request.style)
            
            return PresentationResponse(
                success=True,
                message="Presentation generated successfully",
                file_path=file_path,
                download_url=f"/api/v1/presentation/download/{os.path.basename(file_path)}"
            )
        else:
            raise HTTPException(
                status_code=501,
                detail="Google Slides format not yet implemented"
            )
            
    except Exception as e:
        app_logger.error(f"Error generating presentation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_presentation(filename: str):
    """Download generated presentation."""
    file_path = _pptx_generator.output_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "llm_provider": settings.llm_provider,
        "version": settings.app_version
    }

