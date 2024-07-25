from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: Optional[bool] = True
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: Optional[bool] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None


class CompanyInDB(CompanyBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class VisibilityUpdate(BaseModel):
    visibility: bool
