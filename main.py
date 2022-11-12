from fastapi import FastAPI
from mangum import Mangum

from db import users as db_users
from models import User

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
