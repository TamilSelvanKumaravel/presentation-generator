"""
Debug script to analyze PPTX generation and identify design issues.
"""
from src.services.llm.prompts import build_presentation_prompt
from src.models.schemas import LLMResponse, SlideData
from src.services.presentation.pptx_generator import PPTXGenerator
import json

# Create a simple test presentation
test_response = LLMResponse(
    title="Design Analysis Test",
    summary="Testing Gamma-style layout",
    slides=[
        SlideData(
            slide_number=1,
            title="Test Slide",
            content=["Point 1", "Point 2", "Point 3"],
            image_query="artificial intelligence",
            layout="content"
        )
    ]
)

# Generate presentation
generator = PPTXGenerator()
output_path = generator.generate(test_response)

print(f"\n✓ Generated test presentation: {output_path}")
print("\nAnalyzing design elements...")
print("\nCurrent Design Configuration:")
print("=" * 50)
print("Background: Slate 900 (15, 23, 42)")
print("Card Background: Slate 800 (30, 41, 59)")
print("Accent Violet: (139, 92, 246)")
print("Accent Pink: (236, 72, 153)")
print("Text White: (248, 250, 252)")
print("\nCard Dimensions:")
print("- Title Slide Card: 7\" x 3.5\" at (1.5\", 2\")")
print("- Content Slide Card: 9\" x 5.7\" at (0.5\", 1.3\")")
print("\nDecorative Elements:")
print("- Violet blob: 6\" x 6\" (title) / 4\" x 4\" (content)")
print("- Blue blob: 5\" x 5\" (title only)")
print("- Pink accent line: 0.15\" width")
print("- Violet accent bar: 9\" x 0.08\"")
print("\nPotential Issues to Check:")
print("1. Are blobs too bright? (brightness = -0.5 to -0.6)")
print("2. Is card z-order correct? (should be behind text)")
print("3. Is text positioned inside cards properly?")
print("4. Are colors too saturated?")
print("\nPlease open the generated file and describe what you see!")
