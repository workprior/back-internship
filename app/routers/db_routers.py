from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as redis
from app.db.postgres_init import get_session 
from app.db.redis_init import redis_client
from app.core.config import logger

router = APIRouter()

@router.get("/check-postgres")
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

@router.get("/check-redis")
async def check_redis():
    try:
        # Ping Redis to check the connection
        await redis_client.redis.ping()
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