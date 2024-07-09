import logging
from fastapi import FastAPI, Depends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.db.config import settings

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app setup
app = FastAPI()

# Додано тайм-аут для підключення до PostgreSQL
engine = create_async_engine(settings.POSTGRES_DATABASE_URL, echo=False, connect_args={"timeout": 5})
print(settings.POSTGRES_DATABASE_URL)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

redis_client = None

async def connect_to_redis():
    global redis_client
    try:
        # Додано тайм-аут для підключення до Redis
        redis_client = redis.from_url(settings.REDIS_DATABASE_URL, socket_timeout=5)
        await redis_client.ping()
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")

# Function to disconnect from Redis
async def disconnect_from_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Disconnected from Redis")

# Create tables in the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def disconnect_postgres():
    await engine.dispose()
    logger.info("Disconnected from PostgreSQL")

@app.on_event("startup")
async def on_startup():
    await init_db()
    await connect_to_redis()

@app.on_event("shutdown")
async def on_shutdown():
    await disconnect_postgres()
    await disconnect_from_redis()

@app.get("/")
def root():
    return {
        "status": 200,
        "details": "ok",
        "result": "working"
    }

@app.get("/check-postgres")
async def check_db(session: AsyncSession = Depends(get_session)):
    try:
        # Execute a simple query to check the connection
        result = await session.execute(text("SELECT 1"))
        # Fetch the result
        result.scalar()
        return {
            "status": 200,
            "details": "ok",
            "result": "PostgreSQL connection is working"
        }
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        return {
            "status": 500,
            "details": "error",
            "result": f"Failed to connect to PostgreSQL: {e}"
        }

@app.get("/check-redis")
async def check_redis():
    global redis_client
    try:
        # Ping Redis to check the connection
        await redis_client.ping()
        return {
            "status": 200,
            "details": "ok",
            "result": "Redis connection is working"
        }
    except (redis.ConnectionError, redis.TimeoutError) as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return {
            "status": 500,
            "details": "error",
            "result": f"Failed to connect to Redis: {e}"
        }
