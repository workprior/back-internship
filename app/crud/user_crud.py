from datetime import datetime
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import logger
from app.core.exception import (
    UserEmailAlreadyExistsError,
    UserNotFoundError,
    UserPhoneAlreadyExistsError,
)
from app.core.security import get_password_hash, oauth2_scheme, verify_password
from app.db.models import User
from app.db.postgres_init import get_session
from app.schemas.user_schemas import UserBase, UserCreate, UserSchema, UserUpdateRequest
from app.utils.auth0 import get_auth0_decoded_token
from app.utils.jwt_utils import decode_jwt


async def create_user(session: AsyncSession, user: UserCreate):
    logger.info(f"Creating user with email: {user.email}")
    await check_user_exists(session, user.email, user.phone)
    db_user = User(
        username=user.username,
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        is_active=user.is_active,
        city=user.city,
        phone=user.phone,
        avatar=user.avatar,
        is_superuser=user.is_superuser,
        hashed_password=get_password_hash(user.password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    logger.info(f"User created with ID: {db_user.id}")
    return db_user


async def get_user_by_id(session: AsyncSession, id: int):
    logger.info(f"Get user with ID: {id}")
    result = await session.execute(select(User).filter(User.id == id))
    db_user = result.scalars().first()
    if db_user is None:
        raise UserNotFoundError(user_id=id)
    logger.info(f"User with ID: {id} found")
    return db_user


async def get_all_users(session: AsyncSession, skip: int = 0, limit: int = 10):
    logger.info(f"Get all users")
    result = await session.execute(select(User))
    return paginate(result.scalars().all())


async def change_user_info(session: AsyncSession, id: int, user_update: UserUpdateRequest):
    logger.info(f"Updating user with ID: {id}")
    await check_user_exists(session, user_update.email, user_update.phone)
    result = await session.execute(select(User).filter(User.id == id))
    db_user = result.scalars().first()

    if db_user:
        db_user.username = user_update.username
        db_user.email = user_update.email
        db_user.firstname = user_update.firstname
        db_user.lastname = user_update.lastname
        db_user.city = user_update.city
        db_user.phone = user_update.phone
        db_user.avatar = user_update.avatar
        db_user.updated_at = datetime.utcnow()
        await session.commit()
        logger.info(f"User with ID: {id} updated")
        return db_user


async def delete_user_from_id(session: AsyncSession, id: int):
    logger.info(f"Delete user with ID: {id}")
    result = await session.execute(select(User).filter(User.id == id))
    db_user = result.scalars().first()
    if db_user is None:
        raise UserNotFoundError(user_id=id)
    await session.delete(db_user)
    await session.commit()
    logger.info(f"User with ID: {id} deleted")
    return {"status_code": "200", "detail": "User deleted successfully"}


async def check_user_exists(session: AsyncSession, email: str = None, phone: str = None):
    if email:
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        if user:
            raise UserEmailAlreadyExistsError(email=email)

    if phone:
        result = await session.execute(select(User).filter(User.phone == phone))
        user = result.scalars().first()
        if user:
            raise UserPhoneAlreadyExistsError(phone=phone)


# Validate Auth User
async def validate_auth_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    unauth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password"
    )
    res = await session.execute(select(User).filter(User.username == user.username))
    db_user = res.scalars().first()
    if db_user is None:
        raise unauth
    if not verify_password(user.password, db_user.hashed_password):
        raise unauth

    return db_user


async def get_current_token_payload(
    security_scopes: SecurityScopes,
    token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
):
    try:
        return decode_jwt(token.credentials)
    except:
        return get_auth0_decoded_token(security_scopes, token)


async def get_current_user(
    payload: Annotated[UserBase, Depends(get_current_token_payload)],
    session: AsyncSession = Depends(get_session),
):
    email: str | None = payload.get("email")
    res = await session.execute(select(User).filter(User.email == email))
    db_user = res.scalars().first()
    if db_user is None:
        db_user = UserCreate(
            username="None",
            email=email,
            firstname="None",
            lastname="None",
            city="None",
            phone="None",
            avatar="None",
        )
        db_user = await create_user(session, db_user)
    return db_user


async def get_current_active_user(
    current_user: Annotated[UserBase, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
