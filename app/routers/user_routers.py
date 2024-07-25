from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user_crud import (
    change_user_info,
    create_user,
    delete_user_from_id,
    get_all_users,
    get_current_active_user,
    get_user_by_id,
    validate_auth_user,
)
from app.db.postgres_init import get_session
from app.schemas.jwt_schemas import TokenInfo
from app.schemas.user_schemas import UserCreate, UserInfo, UserUpdateRequest
from app.utils.jwt_utils import encode_jwt

crud_user = APIRouter(prefix="/user")


@crud_user.post("/", response_model=UserInfo)
async def create_users(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await create_user(session, user)


@crud_user.get("/{user_id}/", response_model=UserInfo)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_user_by_id(session, user_id)


@crud_user.get("s/", response_model=LimitOffsetPage[UserInfo])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await get_all_users(session=session)


@crud_user.put("/{user_id}/update/", response_model=UserUpdateRequest)
async def update_user(
    user_id: int, user_update: UserUpdateRequest, session: AsyncSession = Depends(get_session)
):
    return await change_user_info(session, user_id, user_update)


@crud_user.delete("/{user_id}/")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await delete_user_from_id(session, user_id)


@crud_user.post("/login/", response_model=TokenInfo)
async def login(user=Depends(validate_auth_user)):
    jwt_payload = {"sub": user.id, "username": user.username, "email": user.email}
    token = encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="bearer")


@crud_user.get("/me", response_model=UserInfo)
async def get_me(current_user: Annotated[UserInfo, Depends(get_current_active_user)]):
    return current_user


@crud_user.put("/me/update", response_model=UserUpdateRequest)
async def update_me(
    user_update: UserUpdateRequest,
    user: Annotated[UserInfo, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await change_user_info(session, user.id, user_update)


@crud_user.delete("/me/delete")
async def delete_me(
    user: Annotated[UserInfo, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await delete_user_from_id(session, user.id)


@crud_user.get("/callback")
def public():
    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! " "You don't need to be authenticated to see this."),
    }
    return result
