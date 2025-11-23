import os
from src.services.presentation.pptx_generator import PPTXGenerator
from src.models.schemas import LLMResponse, SlideContent

def verify_fixes():
    generator = PPTXGenerator()
    
    # Test cases
    slides = [
        # Slide 1: Title Slide Overlap Check
        # (This is checked by the title slide generation logic itself, which uses the presentation title)
        
        # Slide 2: Consistency Check (Short + Long)
        SlideContent(
            slide_number=1,
            title="Consistency Check",
            content=[
                "Short content.",
                "This is a much longer content item that should force the font size down for BOTH boxes to ensure consistency across the slide."
            ],
            image_query="test"
        ),
        
        # Slide 3: All Short (Should be large font)
        SlideContent(
            slide_number=2,
            title="All Short Content",
            content=[
                "Short item 1",
                "Short item 2"
            ],
            image_query="test"
        ),
        
        # Slide 4: All Long (Should be small font)
        SlideContent(
            slide_number=3,
            title="All Long Content",
            content=[
                "Long item 1 that takes up a lot of space and requires smaller font.",
                "Long item 2 that also takes up a lot of space and requires smaller font."
            ],
            image_query="test"
        )
    ]
        
    response = LLMResponse(
        title="Overlap and Consistency Verification",
        summary="Verifying title overlap fix and uniform font sizing.",
        slides=slides
    )
    
    output_path = generator.generate(response)
    print(f"Verification presentation saved to: {output_path}")

if __name__ == "__main__":
    verify_fixes()
