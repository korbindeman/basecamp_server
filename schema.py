from pydantic import BaseModel


class SensorData(BaseModel):
    node: int
    timestamp: int
    temperature: float
    humidity: float
    pressure: float

    class Config:
        orm_mode = True
