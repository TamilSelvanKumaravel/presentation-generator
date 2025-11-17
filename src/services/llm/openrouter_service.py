"""OpenRouter LLM service implementation."""
import json
import httpx
from typing import Optional
from src.services.llm.base import BaseLLMService
from src.models.schemas import LLMResponse, SlideContent
from src.services.llm.prompts import build_presentation_prompt, build_system_prompt
from src.utils.logger import app_logger


class OpenRouterService(BaseLLMService):
    """OpenRouter service for generating presentation content."""
    
    def __init__(self, api_key: str, model: str = "google/gemini-pro"):
        """Initialize OpenRouter service."""
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        app_logger.info(f"Initialized OpenRouter service with model: {model}")
    
    async def generate_presentation_content(
        self,
        topic: str,
        number_of_slides: int,
        style: str = "professional",
        language: str = "English"
    ) -> LLMResponse:
        """Generate presentation content using OpenRouter."""
        try:
            prompt = build_presentation_prompt(topic, number_of_slides, style, language)
            system_prompt = build_system_prompt()
            
            app_logger.info(f"Generating presentation with OpenRouter for topic: {topic}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.3,  # Lower temperature for more consistent JSON
                        "max_tokens": 4000
                    },
                    timeout=60.0
                )
                
                if response.status_code != 200:
                    raise ValueError(f"OpenRouter API error: {response.text}")
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                if not content:
                    raise ValueError("Empty response from OpenRouter")
                
                # Clean the response - remove any non-ASCII characters that might cause issues
                content_clean = content.encode('ascii', 'ignore').decode('ascii')
                
                data = json.loads(content_clean)
                llm_response = self._parse_response(data)
                
                app_logger.info(f"Successfully generated {len(llm_response.slides)} slides")
                return llm_response
                
        except Exception as e:
            app_logger.error(f"Error generating presentation with OpenRouter: {str(e)}")
            raise
    
    def _parse_response(self, data: dict) -> LLMResponse:
        """Parse LLM response into structured format, handling common typos."""
        slides = []
        
        # Handle different response formats and typos
        slides_data = data.get("slides", [])
        
        for idx, slide_data in enumerate(slides_data, 1):
            # Fix common typos in field names
            slide_number = slide_data.get("slide_number") or slide_data.get("slide极umber") or idx
            title = slide_data.get("title") or slide_data.get("tit1e") or f"Slide {idx}"
            
            # Handle content field (could be array or string)
            content = slide_data.get("content", [])
            if not isinstance(content, list):
                # If content is a string, split it into bullet points
                if isinstance(content, str):
                    content = [point.strip() for point in content.split('\n') if point.strip()]
                else:
                    content = [str(content)]
            
            slides.append(SlideContent(
                slide_number=slide_number,
                title=title,
                content=content
            ))
        
        return LLMResponse(
            title=data.get("title", "Untitled Presentation"),
            summary=data.get("summary", ""),
            slides=slides
        )
    
    async def close(self):
        """Close any resources."""
        pass
