"""Base class for LLM services."""
from abc import ABC, abstractmethod
from typing import Optional
from src.models.schemas import LLMResponse


class BaseLLMService(ABC):
    """Abstract base class for LLM services."""
    
    @abstractmethod
    async def generate_presentation_content(
        self,
        topic: str,
        number_of_slides: int,
        style: str = "professional",
        language: str = "English"
    ) -> LLMResponse:
        """Generate presentation content using LLM."""
        pass
    
    @abstractmethod
    async def close(self):
        """Close any resources."""
        pass


# Add better error handling for JSON parsing
import json
import re

def parse_llm_response(text: str) -> dict:
    """Parse LLM response, handling malformed JSON."""
    try:
        # Try direct JSON parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        # Extract JSON from text if wrapped
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        raise ValueError("LLM response is not valid JSON")