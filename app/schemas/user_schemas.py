from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    firstname: Optional[str] = Field(default="")
    lastname: Optional[str] = Field(default="")
    city: Optional[str] = Field(default="")
    phone: Optional[str] = Field(default="")
    avatar: Optional[str] = Field(default="")
    is_superuser: bool = False


class UserCreate(UserBase):
    hashed_password: str = None


class UserInfo(UserBase):
    model_config = ConfigDict(strict=True)
    id: int


class UserUpdateRequest(BaseModel):
    username: str
    hashed_password: str
    firstname: str
    lastname: str
    city: str = None
    phone: str = None
    avatar: str = None


class SignUpRequest(UserCreate):
    pass


class UserSchema(BaseModel):
    username: str
    hashed_password: str

    model_config = ConfigDict(strict=True)


# class UsersListResponse(BaseModel):
#     users: List[User]
