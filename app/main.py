import codecs
import secrets

from fastapi import Depends, FastAPI, Query, HTTPException
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

app = FastAPI(redoc_url=None, swagger_ui_parameters={"defaultModelsExpandDepth": -1})


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index():
    html = codecs.open("app/html/index.html", "r")
    return html.read()


@app.get("/sensors", response_model=list[SensorDataRead])
async def sensors_get(
    node_id: list[int] | None = Query(default=None),
    _from: int | None = Query(default=None, alias="from"),
    to: int | None = None,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(SensorData))
    data = result.scalars().all()

    if node_id is not None:
        data = [data for data in data if data.node_id in node_id]

    if _from is not None:
        data = [data for data in data if data.timestamp >= _from]

    if to is not None:
        data = [data for data in data if data.timestamp <= to]

    return data


@app.post("/sensors", status_code=201, response_model=SensorData)
async def sensors_post(
    sensor_data: SensorDataCreate,
    key: str,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Nodes))
    nodes = result.scalars().all()
    for node in nodes:
        if key != node.key:
            continue
        db_sensor_data = SensorData.from_orm(sensor_data, {"node_id": node.id})
        try:
            session.add(db_sensor_data)
            await session.commit()
            await session.refresh(db_sensor_data)
        except Exception:
            raise HTTPException(
                status_code=403,
                detail="Sensor data already exists at that timestamp for this node",
            )

        return db_sensor_data
    raise HTTPException(status_code=304, detail="Invalid key")


@app.delete("/sensors")
async def delete(
    key: str,
    timestamp: list[int] = Query(),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Nodes))
    nodes = result.scalars().all()
    for node in nodes:
        if key != node.key:
            continue
        for single_timestamp in timestamp:
            sensor_data = await session.get(SensorData, [node.id, single_timestamp])
            if not sensor_data:
                raise HTTPException(status_code=404, detail="Sensor data not found")
            await session.delete(sensor_data)
            await session.commit()
        return {"ok": True}
    raise HTTPException(status_code=304, detail="Invalid key")



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

    try:
        session.add(db_node_data)
        await session.commit()
        await session.refresh(db_node_data)
    except Exception:
        raise HTTPException(status_code=403, detail="Title is already in use.")
    return db_node_data
