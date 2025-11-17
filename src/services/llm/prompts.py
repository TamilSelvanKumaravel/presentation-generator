"""Prompt templates for LLM generation."""
from typing import Dict


# def build_presentation_prompt(
#     topic: str,
#     number_of_slides: int,
#     style: str,
#     language: str
# ) -> str:
#     """Build prompt for presentation generation."""
    
#     style_guidance = {
#         "professional": "Use formal language, data-driven insights, and business terminology.",
#         "casual": "Use conversational tone, relatable examples, and friendly language.",
#         "academic": "Use scholarly language, citations, and research-based content."
#     }
    
#     prompt = f"""Create a comprehensive presentation about "{topic}" with exactly {number_of_slides} slides.

# Requirements:
# - Language: {language}
# - Style: {style_guidance.get(style, style_guidance['professional'])}
# - Each slide should have a clear title and 3-5 bullet points
# - Content should be informative, well-structured, and engaging
# - First slide should be an introduction, last slide should be a conclusion

# Return a JSON object with this exact structure:
# {{
#     "title": "Presentation Title",
#     "summary": "Brief 2-3 sentence summary of the presentation",
#     "slides": [
#         {{
#             "slide_number": 1,
#             "title": "Slide Title",
#             "content": ["Point 1", "Point 2", "Point 3"]
#         }}
#     ]
# }}

# Ensure all {number_of_slides} slides are included and numbered sequentially."""
    
#     return prompt


def build_presentation_prompt(
    topic: str,
    number_of_slides: int,
    style: str,
    language: str
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
            "content": ["Point 1", "Point 2", "Point 3"]
        }}
    ]
}}

CRITICAL: Use only ASCII characters and proper JSON syntax. No special characters in field names.
Ensure all {number_of_slides} slides are included and numbered sequentially."""
    
    return prompt


def build_system_prompt() -> str:
    """Build system prompt for LLM."""
    return """You are an expert presentation content creator. 
You specialize in creating well-structured, engaging, and informative presentation content.
Always respond with valid JSON that matches the requested structure exactly.
Ensure content is accurate, relevant, and appropriate for the target audience."""

