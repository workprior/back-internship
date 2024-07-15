from typing import List, Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    firstname: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class SignInRequest(BaseModel):
    firstname: str
    password: str


class SignUpRequest(UserCreate):
    pass


class UserUpdateRequest(UserBase):
    firstname: Optional[str] = None


# class UsersListResponse(BaseModel):
#     users: List[User]


class UserDetailsResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
