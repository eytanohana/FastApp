from dotenv import load_dotenv
from pathlib import Path
from sqlmodel import create_engine, Session

import os

load_dotenv(Path(__file__).parent / '.env')
DB_URL = os.environ.get('DB_CONNECTION_URL')

engine = create_engine(DB_URL, echo=True)


def get_db_session():
    with Session(engine) as session:
        yield session
