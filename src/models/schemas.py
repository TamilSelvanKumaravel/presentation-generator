"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class SlideContent(BaseModel):
    """Individual slide content."""
    slide_number: int = Field(..., ge=1, description="Slide number")
    title: str = Field(..., min_length=1, description="Slide title")
    content: List[str] = Field(..., min_items=1, description="Slide bullet points")
    image_query: Optional[str] = Field(None, description="Search query for slide image")
    layout: Literal["title", "content", "two_column", "image_right"] = Field("content", description="Slide layout type")


class PresentationRequest(BaseModel):
    """Request model for presentation generation."""
    topic: str = Field(..., min_length=1, description="Presentation topic")
    number_of_slides: int = Field(5, ge=1, le=50, description="Number of slides")
    format: Literal["pptx", "google-slides"] = Field("pptx", description="Output format")
    style: Literal["professional", "casual", "academic"] = Field(
        "professional", description="Presentation style"
    )
    language: str = Field("English", description="Presentation language")
    include_images: bool = Field(False, description="Include images in slides")


class LLMResponse(BaseModel):
    """LLM response structure."""
    title: str = Field(..., description="Presentation title")
    summary: str = Field(..., description="Brief summary")
    slides: List[SlideContent] = Field(..., min_items=1, description="Slide contents")


class PresentationResponse(BaseModel):
    """Response model for presentation generation."""
    success: bool
    message: str
    presentation_id: Optional[str] = None
    file_path: Optional[str] = None
    download_url: Optional[str] = None

