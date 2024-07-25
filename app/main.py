from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi_pagination import add_pagination

from app.core.config import logger
from app.core.exception import (
    CompanyNameAlreadyExistsError,
    CompanyNotFoundError,
    EmailUserNotFoundError,
    UserEmailAlreadyExistsError,
    UserNoPremissionError,
    UserNotFoundError,
    UserPhoneAlreadyExistsError,
)
from app.db.postgres_init import disconnect_postgres
from app.db.redis_init import redis_client
from app.routers.check_routers import health_check
from app.routers.company_routers import company_router
from app.routers.user_routers import crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
app.include_router(company_router)
add_pagination(app)


@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    logger.error(f"User with id {exc.user_id} not found")
    return JSONResponse(
        status_code=404,
        content={"detail": f"User with id {exc.user_id} not found"},
    )


@app.exception_handler(EmailUserNotFoundError)
async def email_user_not_found_exception_handler(request: Request, exc: EmailUserNotFoundError):
    logger.error(f"User with email {exc.email} not found")
    return JSONResponse(
        status_code=404,
        content={"detail": f"User with id {exc.email} not found"},
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


@app.exception_handler(CompanyNameAlreadyExistsError)
async def name_already_exists_exception_handler(
    request: Request, exc: CompanyNameAlreadyExistsError
):
    logger.error(f"User with email {exc.name} already exists")
    return JSONResponse(
        status_code=400,
        content={"detail": f"User with email {exc.name} already exists"},
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


@app.exception_handler(CompanyNotFoundError)
async def phone_already_exists_exception_handler(request: Request, exc: CompanyNotFoundError):
    logger.error(f"Company with id {exc.id} not found")
    return JSONResponse(
        status_code=400,
        content={"detail": f"Company with id {exc.id} not found"},
    )


@app.exception_handler(UserNoPremissionError)
async def phone_already_exists_exception_handler(request: Request, exc: UserNoPremissionError):
    logger.error(f"You cant update company with id {exc.id}")
    return JSONResponse(
        status_code=400,
        content={"detail": f"You cant update company with id {exc.id} not found"},
    )
