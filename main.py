from fastapi import FastAPI

from db import users as db_users

app = FastAPI()


@app.get('/users')
async def get_users(amount_: int = None):
    if amount_:
        return db_users[:amount_]
    return db_users

