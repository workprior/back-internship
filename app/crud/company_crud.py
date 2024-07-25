from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.company_schemas import CompanyCreate, CompanyInDB
from app.schemas.user_schemas import UserInfo


async def crud_create_company(session: AsyncSession, company: CompanyCreate, user_id: int):
    return user_id
