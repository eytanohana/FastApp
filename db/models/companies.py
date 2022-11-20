from sqlmodel import SQLModel, Field, Relationship

from typing import Optional, TYPE_CHECKING, List
if TYPE_CHECKING:
    from .users import User


class CompanyBase(SQLModel):
    name: str = Field(unique=True)
    headquarters: Optional[str] = None


class Company(CompanyBase, table=True):
    __tablename__ = 'companies'
    company_id: Optional[int] = Field(default=None, primary_key=True)

    users: List['User'] = Relationship(back_populates='company')


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    company_id: int


class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    headquarters: Optional[str] = None
