from sqlmodel import SQLModel, Field

from typing import Optional


class CompanyBase(SQLModel):
    name: str = Field(unique=True)
    headquarters: Optional[str] = None


class Company(CompanyBase, table=True):
    __tablename__ = 'companies'
    company_id: Optional[int] = Field(default=None, primary_key=True)


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    company_id: int


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    headquarters: Optional[str] = None
