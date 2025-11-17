"""PowerPoint presentation generator using python-pptx."""
import os
from pathlib import Path
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.dml.color import RGBColor
from src.models.schemas import LLMResponse
from src.utils.logger import app_logger


class PPTXGenerator:
    """Generate PowerPoint presentations from LLM content."""
    
    def __init__(self, output_dir: str = "presentations"):
        """Initialize PPTX generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        app_logger.info(f"PPTX Generator initialized with output dir: {output_dir}")
    
    def generate(
        self,
        llm_response: LLMResponse,
        style: str = "professional"
    ) -> str:
        """Generate PPTX file from LLM response."""
        try:
            # Create presentation
            prs = Presentation()
            prs.slide_width = Inches(10)
            prs.slide_height = Inches(7.5)
            
            # Set theme colors based on style
            colors = self._get_style_colors(style)
            
            # Title slide
            self._create_title_slide(prs, llm_response.title, llm_response.summary, colors)
            
            # Content slides
            for slide_data in llm_response.slides:
                self._create_content_slide(prs, slide_data, colors)
            
            # Save presentation
            filename = self._generate_filename(llm_response.title)
            filepath = self.output_dir / filename
            prs.save(str(filepath))
            
            app_logger.info(f"Presentation saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            app_logger.error(f"Error generating PPTX: {str(e)}")
            raise
    
    def _create_title_slide(self, prs: Presentation, title: str, summary: str, colors: dict):
        """Create title slide with manual line breaks ONLY."""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Title box - NO auto-size, use manual breaks
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(1.5), Inches(9), Inches(2.5)  # Fixed height
        )
        title_frame = title_box.text_frame
        title_frame.word_wrap = True
        
        processed_title = self._process_text(title, max_chars_per_line=20)
        title_frame.text = processed_title
        
        title_paragraph = title_frame.paragraphs[0]
        title_paragraph.font.size = Pt(36)
        title_paragraph.font.bold = True
        title_paragraph.font.color.rgb = RGBColor(*colors['primary'])
        title_paragraph.alignment = PP_ALIGN.CENTER
        
        # Summary box - NO auto-size
        if summary:
            summary_box = slide.shapes.add_textbox(
                Inches(1), Inches(4), Inches(8), Inches(1.5)  # Fixed height
            )
            summary_frame = summary_box.text_frame
            summary_frame.word_wrap = True
            
            processed_summary = self._process_text(summary, max_chars_per_line=30)
            summary_frame.text = processed_summary
            
            summary_paragraph = summary_frame.paragraphs[0]
            summary_paragraph.font.size = Pt(18)
            summary_paragraph.font.color.rgb = RGBColor(*colors['secondary'])
            summary_paragraph.alignment = PP_ALIGN.CENTER
    
    def _create_content_slide(self, prs: Presentation, slide_data, colors: dict):
        """Create content slide with manual line breaks ONLY."""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Title - NO auto-size
        title_text = f"{slide_data.slide_number}. {slide_data.title}"
        title_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(0.5), Inches(9), Inches(1.2)  # Fixed height
        )
        title_frame = title_box.text_frame
        title_frame.word_wrap = True
        
        processed_title = self._process_text(title_text, max_chars_per_line=25)
        title_frame.text = processed_title
        
        title_paragraph = title_frame.paragraphs[0]
        title_paragraph.font.size = Pt(28)
        title_paragraph.font.bold = True
        title_paragraph.font.color.rgb = RGBColor(*colors['primary'])
        
        # Content bullets - NO auto-size
        y_position = 1.8
        max_bullets_per_slide = 5
        bullet_points = slide_data.content[:max_bullets_per_slide]
        
        for i, point in enumerate(bullet_points):
            processed_point = self._process_text(point, max_chars_per_line=30)
            
            content_box = slide.shapes.add_textbox(
                Inches(0.8), Inches(y_position), Inches(8.5), Inches(0.8)  # Fixed height
            )
            content_frame = content_box.text_frame
            content_frame.word_wrap = True
            
            content_frame.text = f"• {processed_point}"
            
            content_paragraph = content_frame.paragraphs[0]
            content_paragraph.font.size = Pt(16)
            content_paragraph.font.color.rgb = RGBColor(*colors['text'])
            
            # Calculate position based on line count
            line_count = processed_point.count('\n') + 1
            y_position += 0.4 + (line_count * 0.2)
            
            if y_position > 6.5:
                break
    
    def _get_style_colors(self, style: str) -> dict:
        """Get color scheme based on style."""
        color_schemes = {
            "professional": {
                "primary": (0, 51, 102),      # Dark blue
                "secondary": (102, 153, 204),  # Light blue
                "text": (51, 51, 51)           # Dark gray
            },
            "casual": {
                "primary": (204, 51, 51),      # Red
                "secondary": (255, 153, 51),   # Orange
                "text": (68, 68, 68)           # Gray
            },
            "academic": {
                "primary": (51, 51, 51),       # Black
                "secondary": (128, 128, 128),  # Gray
                "text": (51, 51, 51)           # Dark gray
            }
        }
        return color_schemes.get(style, color_schemes["professional"])
    
    def _generate_filename(self, title: str) -> str:
        """Generate filename from title."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in title)
        safe_title = safe_title.replace(' ', '_')[:50]
        return f"{safe_title}_{timestamp}.pptx"

    def _process_text(self, text: str, max_chars_per_line: int = 35) -> str:
        """Force manual line breaks at character limits - SIMPLE version."""
        if not text:
            return ""
        
        # Clean text
        text = ' '.join(text.split())
        
        # Force line breaks every max_chars_per_line characters
        lines = []
        for i in range(0, len(text), max_chars_per_line):
            line = text[i:i + max_chars_per_line].strip()
            if line:
                lines.append(line)
        
        return '\n'.join(lines)