"""Configuration management using Pydantic Settings."""
from pydantic_settings import BaseSettings
from typing import Literal, Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # LLM Configuration
    llm_provider: Literal["openai", "ollama", "openrouter"] = "openai"
    openai_api_key: str = ""
    openai_base_url: Optional[str] = None  # For OpenRouter compatibility
    openai_model: str = "gpt-3.5-turbo"    # Default OpenAI model
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    # OpenRouter specific (when llm_provider = "openrouter")
    openrouter_model: str = "google/gemini-pro"
    
    # Google Slides
    google_credentials_file: str = ""
    google_slides_enabled: bool = False
    
    # Application
    app_name: str = "Presentation Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

