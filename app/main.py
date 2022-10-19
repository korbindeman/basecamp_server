from fastapi import Depends, FastAPI, Query
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.models import SensorData

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/sensors", response_model=list[SensorData])
async def sensors_get(
    node: list[int] | None = Query(default=None),
    start: int | None = None,
    end: int | None = None,
    session: Session = Depends(get_session),
):
    result = session.exec(select(SensorData)).all()

    if node != None:
        result = [data for data in result if data.node in node]

    if start != None:
        result = [data for data in result if data.timestamp >= start]

    if end != None:
        result = [data for data in result if data.timestamp <= end]

    return result


@app.post("/sensors", status_code=201, response_model=SensorData)
async def sensors_post(
    sensor_data: SensorData,
    session: Session = Depends(get_session),
):
    session.add(sensor_data)
    session.commit()
    session.refresh(sensor_data)
    return sensor_data
