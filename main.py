import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import create_engine, Session, select
from mangum import Mangum

from models import User

load_dotenv(Path(__file__).parent / '.env')
DB_URL = os.environ.get('DB_CONNECTION_URL')
engine = create_engine(DB_URL, echo=True)

app = FastAPI()
aws_lambda_handler = Mangum(app)


@app.get('/users', response_model=list[User])
async def get_users(amount: int = None):
    with Session(engine) as session:
        return session.exec(select(User).limit(amount)).all()


@app.post('/users', response_model=User)
async def add_user(user: User):
    with Session(engine) as session:
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='User already taken')
        session.refresh(user)
        return user
