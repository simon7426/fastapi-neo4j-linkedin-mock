import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", False)
    database_url: AnyUrl = os.getenv("DATABASE_URL", "bolt://localhost:7687")
    database_user: str = os.getenv("DATABASE_USER", "neo4j")
    database_password: str = os.getenv("DATABASE_PASSWORD", "brilliant")
    secret: str = os.getenv("SECRET_KEY", "brilliant")
    expiration: int = os.getenv("EXPIRATION_TIME", 3000)


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
