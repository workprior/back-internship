from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings, logger

Base = declarative_base()

# Додано тайм-аут для підключення до PostgreSQL
engine = create_async_engine(settings.POSTGRES_DATABASE_URL, echo=False, connect_args={"timeout": 5})

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def connect_to__postgres():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def disconnect_postgres():
    await engine.dispose()
    logger.info("Disconnected from PostgreSQL")







