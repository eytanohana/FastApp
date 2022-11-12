from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = 'users'

    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: Optional[EmailStr] = Field(unique=True)
    phone_number: Optional[str] = Field(unique=True)
    zip_code: Optional[str] = None
    country: Optional[str] = None
    birthday: Optional[datetime] = None
