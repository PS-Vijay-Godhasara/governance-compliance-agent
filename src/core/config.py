"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Governance Compliance Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # LLM Configuration
    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "mistral:7b"  # mistral:7b, llama3.2:3b, llama3.2:1b, codellama:7b
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: str = "http://localhost:11434"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    
    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-sonnet-20240229"
    
    # Database
    DATABASE_URL: str = "postgresql://governance:password@localhost:5432/governance_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    
    # Performance
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 100
    CACHE_TTL: int = 3600
    
    # Monitoring
    ENABLE_TRACING: bool = True
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 8001
    
    # Policy Configuration
    POLICY_STORE_PATH: str = "./policies"
    SCHEMA_STORE_PATH: str = "./schemas"
    RULES_RELOAD_INTERVAL: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()