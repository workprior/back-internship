from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.core.config import logger
from app.core.exception import (
    UserEmailAlreadyExistsError,
    UserNotFoundError,
    UserPhoneAlreadyExistsError,
)
from app.db.postgres_init import disconnect_postgres
from app.db.redis_init import redis_client
from app.routers.check_routers import health_check
from app.routers.crud_routers import crud_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start app

    await redis_client.connect_redis()

    yield
    # finish app
    await disconnect_postgres()
    await redis_client.disconnect_redis()


# FastAPI app setup
app = FastAPI(lifespan=lifespan)

app.include_router(health_check)
app.include_router(crud_user)
add_pagination(app)


@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    logger.error(f"User with id {exc.user_id} not found")
    return JSONResponse(
        status_code=404,
        content={"detail": f"User with id {exc.user_id} not found"},
    )


@app.exception_handler(UserEmailAlreadyExistsError)
async def email_already_exists_exception_handler(
    request: Request, exc: UserEmailAlreadyExistsError
):
    logger.error(f"User with email {exc.email} already exists")
    return JSONResponse(
        status_code=400,
        content={"detail": f"User with email {exc.email} already exists"},
    )


@app.exception_handler(UserPhoneAlreadyExistsError)
async def phone_already_exists_exception_handler(
    request: Request, exc: UserPhoneAlreadyExistsError
):
    logger.error(f"User with phone {exc.phone} already exists")
    return JSONResponse(
        status_code=400,
        content={"detail": f"User with phone {exc.phone} already exists"},
    )
