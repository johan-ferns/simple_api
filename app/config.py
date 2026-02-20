from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    api_title: str = "Simple API"
    api_version: str = "0.1.0"
    environment: str = "development"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Model settings (for future use)
    model_path: Optional[str] = None
    model_device: str = "cpu"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()