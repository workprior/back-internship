from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    firstname: str
    lastname: str
    city: str = None
    phone: str = None
    avatar: str = None
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserUpdateRequest(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    city: str = None
    phone: str = None
    avatar: str = None


class SignInRequest(BaseModel):
    firstname: str
    password: str


class SignUpRequest(UserCreate):
    pass


# class UsersListResponse(BaseModel):
#     users: List[User]
