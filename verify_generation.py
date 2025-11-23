import sys
import os
sys.path.append(os.getcwd())

from src.services.presentation.pptx_generator import PPTXGenerator
from src.models.schemas import LLMResponse, SlideContent

def verify():
    print("Starting verification...")
    
    # Mock LLM Response
    mock_response = LLMResponse(
        title="Multi-Theme Test",
        summary="Testing random themes and layouts.",
        slides=[
            SlideContent(
                slide_number=1,
                title="Introduction",
                content=["This slide should have an image", "Layout should be two-column", "Theme colors should be consistent"],
                image_query="colorful abstract art",
                layout="content"
            ),
            SlideContent(
                slide_number=2,
                title="Text Only Slide",
                content=["This slide has NO image", "It should use full width", "Text should be readable"],
                image_query=None,
                layout="content"
            )
        ]
    )
    
    generator = PPTXGenerator()
    
    # Generate 3 times to test random themes
    for i in range(3):
        print(f"Generating presentation {i+1}...")
        output_path = generator.generate(mock_response)
        print(f"Success! Generated: {output_path}")

if __name__ == "__main__":
    verify()
