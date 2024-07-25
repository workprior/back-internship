from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud.company_crud import crud_create_company, get_company_by_id
from app.crud.user_crud import get_current_active_user
from app.db.postgres_init import get_session
from app.schemas.company_schemas import CompanyCreate, CompanyInDB
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
