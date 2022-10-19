from fastapi import Depends, FastAPI, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session, init_db
from app.models import SensorData

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/sensors", response_model=list[SensorData])
async def sensors_get(
    node: list[int] | None = Query(default=None),
    start: int | None = None,
    end: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(SensorData))
    data = result.scalars().all()

    if node != None:
        data = [data for data in data if data.node in node]

    if start != None:
        data = [data for data in data if data.timestamp >= start]

    if end != None:
        data = [data for data in data if data.timestamp <= end]

    return data


@app.post("/sensors", status_code=201, response_model=SensorData)
async def sensors_post(
    sensor_data: SensorData,
    session: AsyncSession = Depends(get_session),
):
    session.add(sensor_data)
    await session.commit()
    await session.refresh(sensor_data)
    return sensor_data
