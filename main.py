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
    node: list[int] = Query(default=[]), start: int = 0, end: int = 0
):
    result = db.all()

    if node:
        result = [data for data in result if data["node"] in node]

    if start:
        result = [data for data in result if data["timestamp"] >= start]

    if end:
        result = [data for data in result if data["timestamp"] <= end]

    return result


@app.post("/sensors")
async def sensors_post(sensor_data: SensorData):
    db.insert(vars(sensor_data))
    return sensor_data
