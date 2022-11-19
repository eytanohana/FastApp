from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: Optional[EmailStr] = Field(unique=True)
    phone_number: Optional[str] = Field(unique=True)
    zip_code: Optional[str] = None
    country: Optional[str] = None
    birthday: Optional[datetime] = None


class User(UserBase, table=True):
    __tablename__ = 'users'
    user_id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    user_id: int


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    birthday: Optional[datetime] = None

