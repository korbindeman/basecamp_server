from fastapi import FastAPI, Query
from sqlmodel import Session, SQLModel, create_engine, select
import os
from dotenv import load_dotenv


from models import SensorData

load_dotenv(".env")
engine = create_engine(os.environ["DATABASE_URL"], echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/sensors")
async def sensors_get(
    node: list[int] | None = Query(default=None),
    start: int | None = None,
    end: int | None = None,
):
    with Session(engine) as session:
        result = session.exec(select(SensorData)).all()

        if node != None:
            result = [data for data in result if data.node in node]

        if start != None:
            result = [data for data in result if data.timestamp >= start]

        if end != None:
            result = [data for data in result if data.timestamp <= end]

        return result


@app.post("/sensors", status_code=201, response_model=SensorData)
async def sensors_post(sensor_data: SensorData):
    with Session(engine) as session:
        session.add(sensor_data)
        session.commit()
        session.refresh(sensor_data)
        return sensor_data
