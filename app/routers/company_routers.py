from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.company_crud import (
    crud_create_company,
    crud_delete_company,
    crud_get_all_visible_companys,
    crud_get_company_by_id,
    crud_update_company,
    crud_update_visibility_company,
)
from app.crud.user_crud import get_current_active_user
from app.db.postgres_init import get_session
from app.schemas.company_schemas import (
    CompanyBase,
    CompanyCreate,
    CompanyInDB,
    CompanyUpdate,
    VisibilityUpdate,
)
from app.schemas.user_schemas import UserInfo

company_router = APIRouter(
    prefix="/companies",
)


@company_router.post("/create", response_model=CompanyInDB)
async def create_company(
    company: CompanyCreate,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfo = Depends(get_current_active_user),
):
    return await crud_create_company(session, company, current_user.id)


@company_router.put("/{company_id}/update", response_model=CompanyBase)
async def update_company(
    company_id: int,
    new_company_data: CompanyUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfo = Depends(get_current_active_user),
):
    return await crud_update_company(session, new_company_data, company_id, current_user.id)


@company_router.delete("/{company_id}/delete")
async def delete_company(
    company_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfo = Depends(get_current_active_user),
):
    return await crud_delete_company(session, company_id, current_user.id)


@company_router.patch("/{company_id}/visibility")
async def update_company_visibility(
    company_id: int,
    visibility: VisibilityUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfo = Depends(get_current_active_user),
):
    return await crud_update_visibility_company(session, visibility, company_id, current_user.id)


@company_router.get("/all", response_model=LimitOffsetPage[CompanyBase])
async def get_all_visible_companys(
    session: AsyncSession = Depends(get_session),
    current_user: UserInfo = Depends(get_current_active_user),
):
    return await crud_get_all_visible_companys(session, current_user.id)


@company_router.get("/{company_id}", response_model=CompanyBase)
async def get_company_by_id(
    company_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserInfo = Depends(get_current_active_user),
):
    return await crud_get_company_by_id(session, company_id, current_user.id)
