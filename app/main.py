from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.postgres_init import connect_to__postgres, disconnect_postgres
from app.db.redis_init import redis_client
from app.routers.check_routers import health_check

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start app
    await connect_to__postgres()
    await redis_client.connect_redis()

    yield
    # finish app
    await disconnect_postgres()
    await redis_client.disconnect_redis()

# FastAPI app setup
app = FastAPI(lifespan=lifespan)

app.include_router(health_check)