from fastapi import FastAPI, Query
from pydantic import BaseModel
from tinydb import TinyDB


class SensorData(BaseModel):
    node: int
    timestamp: int
    temperature: float
    humidity: float
    pressure: float


db = TinyDB("db.json")

app = FastAPI()


@app.get("/sensors")
async def sensors_get(
    node: list[int] | None = None, start: int | None = None, end: int | None = None
):
    result = db.all()

    if node != None:
        result = [data for data in result if data["node"] in node]

    if start != None:
        result = [data for data in result if data["timestamp"] >= start]

    if end != None:
        result = [data for data in result if data["timestamp"] <= end]

    return result


@app.post("/sensors", status_code=201)
async def sensors_post(sensor_data: SensorData):
    db.insert(vars(sensor_data))
    return sensor_data
