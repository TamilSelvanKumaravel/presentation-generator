import os
from src.services.presentation.pptx_generator import PPTXGenerator
from src.models.schemas import LLMResponse, SlideContent

def verify_titles():
    generator = PPTXGenerator()
    
    # Test cases with varying title lengths
    titles = [
        "Short Title",
        "Medium Length Title That Should Fit Nicely",
        "A Very Long Title That Might Need Some Font Scaling To Fit In The Box Without Overflowing",
        "Extremely Long Title That Is Definitely Going To Overflow If We Do Not Resize The Font Significantly And It Just Keeps Going And Going"
    ]
    
    slides = []
    for i, title in enumerate(titles):
        slides.append(SlideContent(
            slide_number=i+1,
            title=title,
            content=[f"Content for slide {i+1}"],
            image_query="test" if i % 2 == 0 else None
        ))
        
    response = LLMResponse(
        title="Title Overflow Verification",
        summary="Verifying dynamic font sizing for titles.",
        slides=slides
    )
    
    output_path = generator.generate(response)
    print(f"Verification presentation saved to: {output_path}")

if __name__ == "__main__":
    verify_titles()
