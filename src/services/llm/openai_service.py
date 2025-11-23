"""OpenAI LLM service implementation."""
import json
from typing import Optional
from openai import AsyncOpenAI
from src.services.llm.base import BaseLLMService
from src.models.schemas import LLMResponse, SlideContent
from src.services.llm.prompts import build_presentation_prompt, build_system_prompt
from src.utils.logger import app_logger


class OpenAIService(BaseLLMService):
    """OpenAI service for generating presentation content."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", base_url: Optional[str] = None):
        """Initialize OpenAI service."""
        # For newer OpenAI client versions, we need to handle base_url differently
        if base_url:
            # Create custom client for OpenRouter
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url
            )
        else:
            # Standard OpenAI client
            self.client = AsyncOpenAI(api_key=api_key)
        
        self.model = model
        app_logger.info(f"Initialized OpenAI service with model: {model}")
    
    async def generate_presentation_content(
        self,
        topic: str,
        number_of_slides: int,
        style: str = "professional",
        language: str = "English",
        include_images: bool = True
    ) -> LLMResponse:
        """Generate presentation content using OpenAI."""
        try:
            prompt = build_presentation_prompt(topic, number_of_slides, style, language, include_images)
            system_prompt = build_system_prompt()
            
            app_logger.info(f"Generating presentation for topic: {topic}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
            
            data = json.loads(content)
            llm_response = self._parse_response(data)
            
            app_logger.info(f"Successfully generated {len(llm_response.slides)} slides")
            return llm_response
            
        except Exception as e:
            app_logger.error(f"Error generating presentation with OpenAI: {str(e)}")
            raise
    
    def _parse_response(self, data: dict) -> LLMResponse:
        """Parse LLM response into structured format."""
        slides = []
        for idx, slide_data in enumerate(data.get("slides", []), 1):
            content = slide_data.get("content", [])
            # Ensure content is never empty
            if not content or len(content) == 0:
                content = [f"Content for slide {idx}"]
                app_logger.warning(f"Empty content for slide {idx}, using fallback")
            
            slides.append(SlideContent(
                slide_number=slide_data.get("slide_number", idx),
                title=slide_data.get("title", f"Slide {idx}"),
                content=content,
                image_query=slide_data.get("image_query"),
                layout=slide_data.get("layout", "content")
            ))
        
        return LLMResponse(
            title=data.get("title", "Untitled Presentation"),
            summary=data.get("summary", ""),
            slides=slides
        )
    
    async def close(self):
        """Close any resources."""
        # OpenAI client doesn't need explicit cleanup, but we implement the method
        pass

