from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # Application
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Kryos"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str
    REDIS_MAX_CONNECTIONS: int = 10
    CACHE_TTL: int = 300
    
    # Kafka
    KAFKA_BROKERS: str
    KAFKA_CONSUMER_GROUP: str = "kryos-group"
    KAFKA_TOPIC_MARKET_DATA: str = "market-data"
    KAFKA_TOPIC_PREDICTIONS: str = "predictions"
    
    # API Keys
    BINANCE_API_KEY: str
    BINANCE_SECRET_KEY: str
    COINMARKETCAP_API_KEY: str
    COINGECKO_API_KEY: str
    
    # ML Settings
    MODEL_PATH: str = "/app/models"
    BATCH_SIZE: int = 32
    PREDICTION_INTERVAL: int = 15
    CONFIDENCE_THRESHOLD: float = 0.85
    
    # Rate Limiting
    RATE_LIMIT_PER_SECOND: int = 10
    RATE_LIMIT_BURST: int = 20
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    TELEMETRY_ENABLED: bool = True
    SENTRY_DSN: str | None = None
    
    # Webhook
    WEBHOOK_SECRET: str
    WEBHOOK_RETRY_ATTEMPTS: int = 3
    WEBHOOK_TIMEOUT: int = 5

    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 
