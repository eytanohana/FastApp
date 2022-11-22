from db import get_db_session
from db.models import companies
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, Query, HTTPException, status, APIRouter

companies_router = APIRouter(prefix='/companies', tags=['companies'])


@companies_router.get('', response_model=list[companies.CompanyRead])
def get_companys(session: Session = Depends(get_db_session),
              amount: int = Query(default=10, le=100),
              offset: int = 0):
    return session.exec(select(companies.Company).offset(offset).limit(amount)).all()


@companies_router.get('/{company_id}', response_model=companies.CompanyRead)
def get_company_by_id(*, session: Session = Depends(get_db_session), company_id: int):
    company = session.get(companies.Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    return company


@companies_router.post('', response_model=companies.CompanyRead)
def add_company(*, session: Session = Depends(get_db_session), company: companies.CompanyCreate):
    try:
        company_db = companies.Company.from_orm(company)
        session.add(company_db)
        session.commit()
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Company already taken')
    session.refresh(company_db)
    return company_db


@companies_router.patch('/{company_id}', response_model=companies.CompanyRead)
def update_company(*, session: Session = Depends(get_db_session),
                company_id: int,
                company: companies.CompanyUpdate):
    db_company = session.get(companies.Company, company_id)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    for k, v in company.dict(exclude_unset=True).items():
        setattr(db_company, k, v)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company


@companies_router.delete('/{company_id}')
def delete_company(*, session: Session = Depends(get_db_session), company_id: int):
    company = session.get(companies.Company, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    # session.delete(company)
    # session.commit()
    return {'msg': 'Deletion disabled for now'}
