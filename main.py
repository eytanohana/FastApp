import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine, Session, select
from mangum import Mangum

from models import User, UserRead, UserCreate

load_dotenv(Path(__file__).parent / '.env')
DB_URL = os.environ.get('DB_CONNECTION_URL')
engine = create_engine(DB_URL, echo=True)

app = FastAPI()
aws_lambda_handler = Mangum(app)


@app.get('/users', response_model=list[UserRead])
def get_users(amount: int = Query(default=10, le=100)):
    with Session(engine) as session:
        return session.exec(select(User).limit(amount)).all()


@app.get('/users/{user_id}', response_model=UserRead)
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user


@app.post('/users', response_model=UserRead)
async def add_user(user: UserCreate):
    with Session(engine) as session:
        try:
            user_db = User.from_orm(user)
            session.add(user_db)
            session.commit()
        except IntegrityError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='User already taken')
        session.refresh(user_db)
        return user_db
