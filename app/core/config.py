import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_DB_PORT: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_MAPPED_PORT: str
    LOCALHOST: str

    REDIS_DB_PORT: str
    REDIS_DB_HOST: str

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
    def REDIS_DATABASE_URL(self):
        return f"redis://{self.REDIS_DB_HOST}:{self.REDIS_DB_PORT}"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()


# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
