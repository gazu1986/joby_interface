from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict, Any
import json

class Settings(BaseSettings):
    APP_NAME: str = "Joby Interface Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Kafka Settings
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "sensor_data"
    KAFKA_CONSUMER_GROUP: str = "sensor_group"
    
    # Database Settings
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "joby_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "secret"
    
    # Metrics
    ENABLE_METRICS: bool = False
    METRICS_PORT: int = 9091
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 