import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import create_engine, Session, select
from mangum import Mangum

from db import users as db_users
from models import User

load_dotenv(Path(__file__).parent / '.env')
DB_URL = os.environ.get('DB_CONNECTION_URL')
engine = create_engine(DB_URL, echo=True)

app = FastAPI()
aws_lambda_handler = Mangum(app)


@app.get('/users', response_model=list[User])
async def get_users(amount: int = None):
    users = db_users[:amount] if amount else db_users
    return [User(**user) for user in users]


@app.post('/users', response_model=User)
async def add_user(user: User):
    db_users.append(user.dict())
    return user
