"""Prompt templates for LLM generation."""
from typing import Dict

def build_presentation_prompt(
    topic: str,
    number_of_slides: int,
    style: str,
    language: str,
    include_images: bool = True
) -> str:
    prompt = f"""Create a comprehensive presentation about "{topic}" with exactly {number_of_slides} slides.

Requirements:
- Language: {language}
- Style: {style}
- Each slide should have a clear title and 3-5 bullet points
- Content should be informative, well-structured, and engaging
- First slide should be an introduction, last slide should be a conclusion

IMPORTANT: You MUST return ONLY valid JSON with this exact structure:
{{
    "title": "Presentation Title",
    "summary": "Brief 2-3 sentence summary",
    "slides": [
        {{
            "slide_number": 1,
            "title": "Slide Title", 
            "content": ["Point 1", "Point 2", "Point 3"],
            {f'"image_query": "Search term for a relevant image",' if include_images else ''}
            "layout": "content"  # Options: "title", "content", "two_column", "image_right"
        }}
    ]
}}

CRITICAL: Use only ASCII characters and proper JSON syntax. No special characters in field names.
Ensure all {number_of_slides} slides are included and numbered sequentially.
For the first slide, use layout "title".
For the last slide, use layout "content".
For other slides, choose the most appropriate layout based on content.

IMAGE REQUIREMENTS (VERY IMPORTANT):
{f'''- Include an "image_query" for EVERY slide except the title slide
- Each image_query MUST be highly specific to BOTH the main topic ("{topic}") AND the slide's specific content
- Examples for "{topic}":
  * If slide is about "Current Trends" → image_query: "{topic.lower()} current trends technology"
  * If slide is about "Future Predictions" → image_query: "{topic.lower()} future innovations concept"
  * If slide is about "Benefits" → image_query: "{topic.lower()} benefits advantages"
- ALWAYS include the main topic keywords in the image_query
- Make image queries descriptive and specific (3-6 words)''' if include_images else "Do NOT include 'image_query' field."}
"""
    return prompt


def build_system_prompt() -> str:
    """Build system prompt for LLM."""
    return """You are an expert presentation content creator. 
You specialize in creating well-structured, engaging, and informative presentation content.
Always respond with valid JSON that matches the requested structure exactly.
Ensure content is accurate, relevant, and appropriate for the target audience."""
