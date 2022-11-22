from db import get_db_session
from db.models import users
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, Query, HTTPException, status, APIRouter

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.get('', response_model=list[users.UserRead])
def get_users(session: Session = Depends(get_db_session),
              amount: int = Query(default=10, le=100),
              offset: int = 0):
    return session.exec(select(users.User).offset(offset).limit(amount)).all()


@users_router.get('/{user_id}', response_model=users.UserRead)
def get_user_by_id(*, session: Session = Depends(get_db_session), user_id: int):
    user = session.get(users.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@users_router.post('', response_model=users.UserRead)
def add_user(*, session: Session = Depends(get_db_session), user: users.UserCreate):
    try:
        user_db = users.User.from_orm(user)
        session.add(user_db)
        session.commit()
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='User already taken')
    session.refresh(user_db)
    return user_db


@users_router.patch('/{user_id}', response_model=users.UserRead)
def update_user(*, session: Session = Depends(get_db_session),
                user_id: int,
                user: users.UserUpdate):
    db_user = session.get(users.User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    for k, v in user.dict(exclude_unset=True).items():
        setattr(db_user, k, v)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@users_router.delete('/{user_id}')
def delete_user(*, session: Session = Depends(get_db_session), user_id: int):
    user = session.get(users.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    # session.delete(user)
    # session.commit()
    return {'ok': 'Deletion disabled for now'}
