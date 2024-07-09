from fastapi import FastAPI
from app.db.postgres_init import connect_to__postgres, disconnect_postgres
from app.db.redis_init import redis_client
from app.routers.db_routers import router

# FastAPI app setup
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await connect_to__postgres()
    await redis_client.connect_redis()

@app.on_event("shutdown")
async def on_shutdown():
    await disconnect_postgres()
    await redis_client.disconnect_redis()

@app.get("/")
def root():
    return {
        "status": 200,
        "details": "ok",
        "result": "working"
    }

app.include_router(router)