import logging
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_DB_PORT: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_MAPPED_PORT: str
    LOCALHOST: str

    TEST_POSTGRES_DB_PORT: str
    TEST_POSTGRES_DB_NAME: str

    REDIS_DB_PORT: str
    REDIS_DB_HOST: str

    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: str

    @property
    def POSTGRES_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_MAPPED_PORT}/{self.POSTGRES_DB_NAME}"

    # work with container 'postgresql+asyncpg://user:password@postgres_db:5432/database'
    # work with loc 'postgresql+asyncpg://user:password@localhost:5431/database'

    @property
    def POSTGRES_ALEMBIC_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.LOCALHOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"
        # return f"postgresql+psycopg2://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"

    @property
    def POSTGRES_TEST_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.LOCALHOST}:{self.TEST_POSTGRES_DB_PORT}/{self.TEST_POSTGRES_DB_NAME}"
        # return f"postgresql+psycopg2://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"

    @property
    def REDIS_DATABASE_URL(self):
        return f"redis://{self.REDIS_DB_HOST}:{self.REDIS_DB_PORT}"

    class Config:
        env_file = ".env"
        extra = "ignore"


class JWTToken(BaseModel):
    private_key_path: Path = Path("certs/jwt-private.pem")
    public_key_path: Path = Path("certs/jwt-public.pem")
    algorithm: str = "RS256"
    expire_minutes: int = 30


settings = Settings()

auth_jwt: JWTToken = JWTToken()


# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
