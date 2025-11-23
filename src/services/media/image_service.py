import os
import requests
from pathlib import Path
from typing import Optional
from duckduckgo_search import DDGS
from src.utils.logger import app_logger

class ImageService:
    """Service to fetch and manage images for presentations."""
    
    def __init__(self, cache_dir: str = "media_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ddgs = DDGS()
        
    def get_image(self, query: str, width: int = 800, height: int = 600) -> Optional[str]:
        """
        Search for an image and download it.
        Returns the path to the downloaded image or None if failed.
        """
        import time
        
        retries = 3
        for attempt in range(retries):
            try:
                # Search for images
                app_logger.info(f"Searching for image: {query} (Attempt {attempt + 1})")
                results = self.ddgs.images(
                    query,
                    max_results=1,
                )
                
                if not results:
                    app_logger.warning(f"No images found for query: {query}")
                    return None
                    
                image_url = results[0]['image']
                return self._download_image(image_url, query)
                
            except Exception as e:
                app_logger.error(f"Error fetching image for '{query}': {str(e)}")
                if "403" in str(e) or "Ratelimit" in str(e):
                    time.sleep(3 * (attempt + 1)) # Increased backoff
                    continue
                # If other error, try fallback immediately
                break
        
        app_logger.warning(f"DDGS failed, using fallback for: {query}")
        return self._get_fallback_image(query)

    def _get_fallback_image(self, query: str) -> Optional[str]:
        """Get a fallback image using Pollinations.ai (generative)."""
        try:
            # Use Pollinations.ai to generate an image
            # This ensures relevance even when search fails
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            # Add 'realistic, highly detailed' to prompt to get better presentation images
            enhanced_query = urllib.parse.quote(f"{query}, realistic, 4k, professional photography")
            url = f"https://image.pollinations.ai/prompt/{enhanced_query}?width=800&height=600&nologo=true"
            
            app_logger.info(f"Using Pollinations.ai fallback for: {query}")
            return self._download_image(url, query, timeout=60)
            
        except Exception as e:
            app_logger.error(f"Pollinations fallback failed: {e}")
        except Exception as e:
            app_logger.error(f"Pollinations fallback failed: {e}")
            
            # Try one more time with a simpler prompt and different seed
            try:
                import random
                seed = random.randint(1, 10000)
                # Simplified query to avoid complexity issues
                simple_query = urllib.parse.quote(query)
                url = f"https://image.pollinations.ai/prompt/{simple_query}?width=800&height=600&nologo=true&seed={seed}"
                app_logger.info(f"Retrying Pollinations with simple query: {query}")
                return self._download_image(url, query, timeout=60)
            except Exception as e2:
                app_logger.error(f"Retry failed: {e2}")
                return None
    
    def _download_image(self, url: str, query: str, timeout: int = 15) -> Optional[str]:
        """Download image from URL."""
        try:
            # Create safe filename
            safe_query = "".join(c if c.isalnum() else "_" for c in query)[:30]
            ext = url.split('.')[-1].split('?')[0]
            if len(ext) > 4 or not ext:
                ext = "jpg"
            
            filename = f"{safe_query}.{ext}"
            filepath = self.cache_dir / filename
            
            # Return cached if exists
            if filepath.exists():
                return str(filepath)
            
            # Download
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            app_logger.info(f"Image downloaded: {filepath}")
            return str(filepath)
            
        except Exception as e:
            app_logger.error(f"Error downloading image {url}: {str(e)}")
            return None
