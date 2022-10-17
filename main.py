import uvicorn
from typing import Union
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
    node: Union[list[int], None] = Query(default=None),
    start: Union[int, None] = None,
    end: Union[int, None] = None,
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

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="20.79.107.0", port=8000, reload=False)
