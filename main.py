from fastapi import FastAPI

from db import users as db_users
from models import User

app = FastAPI()


@app.get('/users', response_model=list[User])
async def get_users(amount: int = None):
    users = db_users[:amount] if amount else db_users
    return [User(**user) for user in users]

