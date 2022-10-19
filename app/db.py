import os
from dotenv import load_dotenv

from sqlmodel import create_engine, SQLModel, Session


load_dotenv(".env")
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
