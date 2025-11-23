from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080
    
    # CORS
    frontend_url: str
    production_url: str
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
