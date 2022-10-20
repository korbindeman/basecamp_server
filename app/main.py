import codecs

from fastapi import Depends, FastAPI, Query
from fastapi.responses import HTMLResponse

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session, init_db
from app.models import NodeData, SensorData

app = FastAPI(redoc_url=None)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    html = codecs.open("app/html/index.html", "r")
    return html.read()


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


@app.get("/node", response_model=NodeData | list[NodeData] | None)
async def node_get(
    node: int | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    if not node:
        result = await session.execute(select(NodeData))
        return result.scalars().all()

    result = await session.get(NodeData, node)
    return result


@app.post("/node", status_code=201, response_model=NodeData)
async def node_post(
    node_data: NodeData,
    session: AsyncSession = Depends(get_session),
):
    session.add(node_data)
    await session.commit()
    await session.refresh(node_data)
    return node_data
