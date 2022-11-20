from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from .companies import Company


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: Optional[EmailStr] = Field(unique=True)
    phone_number: Optional[str] = Field(unique=True)
    zip_code: Optional[str] = None
    country: Optional[str] = None
    birthday: Optional[datetime] = None
    company_id: Optional[int] = Field(default=None, foreign_key='companies.company_id')


class User(UserBase, table=True):
    __tablename__ = 'users'
    user_id: Optional[int] = Field(default=None, primary_key=True)

    company: Optional['Company'] = Relationship(back_populates='users')


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

