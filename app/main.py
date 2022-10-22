import codecs
import secrets

from fastapi import Depends, FastAPI, Query
from fastapi.responses import HTMLResponse

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

from app.models import (
    Nodes,
    NodesCreate,
    NodesRead,
    SensorData,
    SensorDataCreate,
    SensorDataRead,
)

app = FastAPI(redoc_url=None)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    html = codecs.open("app/html/index.html", "r")
    return html.read()


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
    key: str,
    sensor_data: SensorDataCreate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Nodes))
    nodes = result.scalars().all()
    for node in nodes:
        if key != node.key:
            continue
        db_sensor_data = SensorData.from_orm(sensor_data, {"node_id": node.id})
        session.add(db_sensor_data)
        await session.commit()
        await session.refresh(db_sensor_data)
        return db_sensor_data


@app.get("/nodes", response_model=list[NodesRead])
async def node_get(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Nodes))
    data = result.scalars().all()

    return data


@app.post("/nodes", status_code=201, response_model=Nodes)
async def node_post(
    node_data: NodesCreate,
    session: AsyncSession = Depends(get_session),
):
    key = secrets.token_urlsafe(16)
    db_node_data = Nodes.from_orm(node_data, {"key": key})

    session.add(db_node_data)
    await session.commit()
    await session.refresh(db_node_data)
    return db_node_data
