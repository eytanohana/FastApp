from fastapi import FastAPI

from .db import users as db_users

app = FastAPI()


@app.get('/users')
async def get_users():
    return db_users

