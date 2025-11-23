import os
from src.services.presentation.pptx_generator import PPTXGenerator
from src.models.schemas import LLMResponse, SlideContent

def verify_overflow():
    generator = PPTXGenerator()
    
    # Test cases with varying title and content lengths
    slides = [
        SlideContent(
            slide_number=1,
            title="Short Title",
            content=["Short content"],
            image_query="test"
        ),
        SlideContent(
            slide_number=2,
            title="Medium Title",
            content=["This is a medium length content that should fit nicely in the box without any issues."],
            image_query="test"
        ),
        SlideContent(
            slide_number=3,
            title="Long Content Test",
            content=["This is a very long content string that is designed to test the dynamic font sizing capabilities of the presentation generator. It should automatically scale down the font size to ensure that the text fits within the allocated box without overflowing or getting cut off. This is a critical feature for ensuring professional-looking slides."],
            image_query="test"
        ),
        SlideContent(
            slide_number=4,
            title="Extremely Long Content Test",
            content=["This is an extremely long content string that goes on and on and on. It is intended to push the limits of the text box and force the font size to be reduced significantly. If the implementation is correct, this text should still be visible and contained within the box, albeit with a much smaller font size. We want to avoid any situation where the text spills out of the container."],
            image_query="test"
        )
    ]
        
    response = LLMResponse(
        title="Content Overflow Verification",
        summary="Verifying dynamic font sizing for content.",
        slides=slides
    )
    
    output_path = generator.generate(response)
    print(f"Verification presentation saved to: {output_path}")

if __name__ == "__main__":
    verify_overflow()
