"""Ollama LLM service implementation for local models."""
import json
from typing import Optional
import ollama
from src.services.llm.base import BaseLLMService
from src.models.schemas import LLMResponse, SlideContent
from src.services.llm.prompts import build_presentation_prompt, build_system_prompt
from src.utils.logger import app_logger

class OllamaService(BaseLLMService):
    """Ollama service for generating presentation content using local LLMs."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "phi3:mini"):
        """Initialize Ollama service."""
        self.base_url = base_url.rstrip('/')
        self.model = model
        # Configure the Ollama client
        self.client = ollama.Client(host=self.base_url)
        app_logger.info(f"Initialized Ollama service: {base_url}, model: {model}")
    
    async def generate_presentation_content(
        self,
        topic: str,
        number_of_slides: int,
        style: str = "professional",
        language: str = "English"
    ) -> LLMResponse:
        """Generate presentation content using Ollama."""
        try:
            prompt = build_presentation_prompt(topic, number_of_slides, style, language)
            system_prompt = build_system_prompt()
            
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            app_logger.info(f"Generating presentation with Ollama for topic: {topic}")
            
            # Use the Ollama client to generate content
            response = self.client.generate(
                model=self.model,
                prompt=full_prompt,
                system=system_prompt,
                stream=False,
                format="json",
                options={
                    "temperature": 0.7,  # Slightly higher for more creative responses
                    "top_p": 0.9,
                    "top_k": 50,
                    "num_ctx": 2048,   # Increased context for better understanding
                    "num_thread": 4,    # Use more threads for better performance
                    "num_gpu": 0,       # Force CPU only
                    "num_predict": 1024,  # Increased output length for better responses
                    "stop": ["<|end|>", "<|assistant|>", "<|user|>"]  # Better stopping criteria for phi3
                },
            )
            
            # Extract the response
            if "response" not in response:
                raise ValueError("Invalid response from Ollama")
            
            content = response["response"]
            
            # Try to parse the response as JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, try to fix common issues
                try:
                    # Try to find JSON in the response
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start >= 0 and end > start:
                        data = json.loads(content[start:end])
                    else:
                        # If no JSON found, create a simple response
                        data = {
                            "title": topic,
                            "summary": content[:200] + "..." if len(content) > 200 else content,
                            "slides": [
                                {
                                    "slide_number": 1,
                                    "title": topic,
                                    "content": [content]
                                }
                            ]
                        }
                except Exception as e:
                    app_logger.error(f"Error parsing Ollama response: {str(e)}")
                    data = {
                        "title": topic,
                        "summary": "Error parsing response",
                        "slides": [
                            {
                                "slide_number": 1,
                                "title": "Error",
                                "content": ["Failed to parse the response. Please try again."]
                            }
                        ]
                    }
            
            llm_response = self._parse_response(data)
            app_logger.info(f"Successfully generated {len(llm_response.slides)} slides")
            return llm_response
            
        except Exception as e:
            app_logger.error(f"Error generating presentation with Ollama: {str(e)}")
            raise
    
    def _parse_response(self, data: dict) -> LLMResponse:
        """Parse LLM response into structured format."""
        # Handle different response formats
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary response, got {type(data).__name__}")
            
        # Check for error in response
        if "error" in data:
            raise ValueError(f"Error from Ollama: {data['error']}")
            
        # Handle case where the response might be nested under a 'response' key
        if "response" in data and isinstance(data["response"], dict):
            data = data["response"]
            
        # Ensure we have slides data
        if "slides" not in data:
            # If no slides key, try to create a single slide with the response
            return LLMResponse(
                title=data.get("title", "Generated Presentation"),
                summary=data.get("summary", ""),
                slides=[
                    SlideContent(
                        slide_number=1,
                        title=data.get("title", "Main Topic"),
                        content=[str(data.get("content", "No content generated"))]
                    )
                ]
            )
            
        # Process slides if they exist
        slides = []
        for idx, slide_data in enumerate(data.get("slides", []), 1):
            # Ensure content is a list
            content = slide_data.get("content", [])
            if not isinstance(content, list):
                content = [str(content)]
                
            slides.append(SlideContent(
                slide_number=slide_data.get("slide_number", idx),
                title=slide_data.get("title", f"Slide {idx}"),
                content=content
            ))
        
        return LLMResponse(
            title=data.get("title", "Untitled Presentation"),
            summary=data.get("summary", ""),
            slides=slides
        )
    
    async def close(self):
        """Close any resources."""
        pass  # The Ollama client doesn't need explicit cleanup

