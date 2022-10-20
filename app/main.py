from random import choices
import string
from fastapi import Depends, FastAPI, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session, init_db
from app.models import (
    NodeData,
    NodeDataCreate,
    NodeDataRead,
    NodeDataReadAfterCreate,
    SensorData,
    SensorDataCreate,
    SensorDataRead,
)
from sqlalchemy import event

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/sensors", response_model=list[SensorDataRead])
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
    sensor_data: SensorDataCreate,
    session: AsyncSession = Depends(get_session),
):
    db_sensor_data = SensorData.from_orm(sensor_data)
    session.add(db_sensor_data)
    await session.commit()
    await session.refresh(db_sensor_data)
    return db_sensor_data


@app.get("/nodes", response_model=NodeData | list[NodeData] | None)
async def node_get(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(NodeData))
    return result.scalars().all()


@app.post("/nodes", status_code=201, response_model=NodeDataReadAfterCreate)
async def node_post(
    node_data: NodeDataCreate,
    session: AsyncSession = Depends(get_session),
):
    db_node_data = NodeData.from_orm(node_data)
    session.add(db_node_data)
    await session.commit()
    await session.refresh(db_node_data)
    return db_node_data


@event.listens_for(NodeData, "before_insert")
def before_insert_node(mapper, connection, target):
    target.key = "".join(choices(string.ascii_letters + string.digits, k=15))
