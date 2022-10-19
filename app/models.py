from sqlmodel import Field, SQLModel


class SensorData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    node: int
    timestamp: int
    temperature: float
    humidity: float
    pressure: float
