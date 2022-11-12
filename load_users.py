from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from pathlib import Path
import os

from db import users
from models import User


load_dotenv(Path(__file__).parent / '.env')
DB_URL = os.environ.get('DB_CONNECTION_URL')
engine = create_engine(DB_URL, echo=True)

with Session(engine) as ses:
    for user in users:
        ses.add(User(**user))
    ses.commit()
