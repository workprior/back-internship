from datetime import datetime

from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import logger
from app.core.exception import (
    UserEmailAlreadyExistsError,
    UserNotFoundError,
    UserPhoneAlreadyExistsError,
)
from app.core.security import get_password_hash
from app.db.models import User
from app.schemas.schemas import UserCreate, UserUpdateRequest


async def create_user(session: AsyncSession, user: UserCreate):
    logger.info(f"Creating user with email: {user.email}")
    await check_user_exists(session, user.email, user.phone)
    db_user = User(
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
