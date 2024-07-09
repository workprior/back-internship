from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_DB_USER : str
    POSTGRES_DB_PASSWORD : str
    POSTGRES_DB_NAME : str
    POSTGRES_DB_PORT : str
    POSTGRES_DB_HOST : str

    REDIS_DB_PORT : str
    REDIS_DB_HOST : str

    @property
    def POSTGRES_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}"
        # return 'postgresql+asyncpg://user:password@localhost:5431/database'
    @property
    def REDIS_DATABASE_URL(self):
        return f"redis://{self.REDIS_DB_HOST}:{self.REDIS_DB_PORT}"

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
