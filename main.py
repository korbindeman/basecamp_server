from fastapi import FastAPI, Query
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import SensorData as SchemaSensorData

from models import SensorData as ModelSensorData

import os
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URI"])


@app.get("/v1/sensors")
async def sensors_get(
    node: list[int] | None = Query(default=None),
    start: int | None = None,
    end: int | None = None,
):
    result = db.session.query(ModelSensorData).all()

    if node != None:
        result = [data for data in result if data.node in node]

    if start != None:
        result = [data for data in result if data.timestamp >= start]

    if end != None:
        result = [data for data in result if data.timestamp <= end]

    return result


@app.post("/v1/sensors", status_code=201, response_model=SchemaSensorData)
async def sensors_post(sensor_data: SchemaSensorData):
    db_sensordata = ModelSensorData(
        node=sensor_data.node,
        timestamp=sensor_data.timestamp,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity,
        pressure=sensor_data.pressure,
    )
    db.session.add(db_sensordata)
    db.session.commit()
    return db_sensordata
