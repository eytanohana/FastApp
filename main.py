from fastapi import FastAPI
from mangum import Mangum

from routers import users_router, companies_router


app = FastAPI()
aws_lambda_handler = Mangum(app)

app.include_router(users_router)
app.include_router(companies_router)
