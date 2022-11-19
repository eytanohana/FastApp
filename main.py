from fastapi import FastAPI
from mangum import Mangum

from routers.users import users_router


app = FastAPI()
aws_lambda_handler = Mangum(app)

app.include_router(users_router)

