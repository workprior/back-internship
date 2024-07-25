from datetime import datetime

from fastapi import Depends
from fastapi_pagination import paginate
from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import logger
from app.core.exception import (
    CompanyNameAlreadyExistsError,
    CompanyNotFoundError,
    UserNoPremissionError,
)
from app.db.models import Company
from app.schemas.company_schemas import CompanyCreate, CompanyInDB, VisibilityUpdate
from app.schemas.user_schemas import UserInfo


async def crud_create_company(session: AsyncSession, company: CompanyCreate, user_id: int):
    logger.info(f"Creating company with name: {company.name}")
    await check_company_exists(session, company.name)
    db_company = Company(
        name=company.name,
        description=company.description,
        address=company.address,
        phone=company.phone,
        email=company.email,
        website=company.website,
        visibility=True,
        owner_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(db_company)
    await session.commit()
    await session.refresh(db_company)
    logger.info(f"Company created with name: {db_company.name}")
    return db_company


async def check_company_exists(session: AsyncSession, name: str = None):
    if name:
        result = await session.execute(select(Company).filter(Company.name == name))
        user = result.scalars().first()
        if user:
            raise CompanyNameAlreadyExistsError(name=name)


async def crud_update_company(
    session: AsyncSession, new_company_data: CompanyInDB, company_id: str, ovner_id: str
):
    logger.info(f"Updating company with ID: {company_id}")
    result = await session.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise CompanyNotFoundError(name=company_id)

    if ovner_id != company.owner_id:
        raise UserNoPremissionError(id=company_id)

    company.name = new_company_data.name
    company.description = new_company_data.description
    company.address = new_company_data.address
    company.phone = new_company_data.phone
    company.email = new_company_data.email
    company.website = new_company_data.website
    company.visibility = new_company_data.visibility
    company.updated_at = datetime.utcnow()
    session.add(company)
    await session.commit()
    await session.refresh(company)
    logger.info(f"Company updated with ID: {company_id}")
    return company


async def crud_delete_company(session: AsyncSession, company_id: str, owner_id: str):
    logger.info(f"Deleting company with ID: {company_id}")
    result = await session.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise CompanyNotFoundError(id=company_id)

    if owner_id != company.owner_id:
        raise UserNoPremissionError(id=company_id)

    await session.delete(company)
    await session.commit()
    logger.info(f"Company deleted with ID: {company_id}")
    return {"status_code": "200", "detail": f"Company deleted with ID: {company_id}"}


async def crud_update_visibility_company(
    session: AsyncSession, visibility: VisibilityUpdate, company_id: str, owner_id: str
):
    logger.info(f"Updating company visibility with ID: {company_id}")
    result = await session.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise CompanyNotFoundError(id=company_id)

    if owner_id != company.owner_id:
        raise UserNoPremissionError(id=company_id)

    company.visibility = visibility.visibility
    company.updated_at = datetime.utcnow()

    session.add(company)
    await session.commit()
    await session.refresh(company)
    logger.info(f"Company visibility updated with ID: {company_id}")
    return company


async def crud_get_all_visible_companys(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Company).filter(
            or_(
                Company.visibility == True,
                and_(Company.visibility == False, Company.owner_id == user_id),
            )
        )
    )
    companys = result.scalars().all()
    return paginate(companys)


async def crud_get_company_by_id(session: AsyncSession, company_id: str, owner_id: str):
    result = await session.execute(select(Company).filter(Company.id == company_id))
    company = result.scalars().first()

    if not company:
        raise CompanyNotFoundError(id=company_id)

    if company.visibility == False and owner_id != company.owner_id:
        raise UserNoPremissionError(id=company_id)

    return company
