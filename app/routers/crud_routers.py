from fastapi import APIRouter, Depends, Query
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user_crud import (
    change_user_info,
    create_user,
    delete_user_from_id,
    get_all_users,
    get_user_by_id,
)
from app.db.postgres_init import get_session
from app.schemas.schemas import User, UserCreate, UserUpdateRequest

crud_user = APIRouter()


@crud_user.post("/user/", response_model=User)
async def create_users(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(session, user)


@crud_user.get("/user/{user_id}/", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_user_by_id(session, user_id)


@crud_user.get("/users/", response_model=LimitOffsetPage[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await get_all_users(session=session)


@crud_user.put("/user/{user_id}/update/", response_model=UserUpdateRequest)
async def update_user(
    user_id: int, user_update: UserUpdateRequest, session: AsyncSession = Depends(get_session)
):
    return await change_user_info(session, user_id, user_update)


@crud_user.delete("/user/{user_id}/")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_user_from_id(session, user_id)
