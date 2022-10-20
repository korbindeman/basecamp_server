import random
import string
from sqlmodel import Field, SQLModel


class SensorData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    node: int
    timestamp: int
    temperature: float
    humidity: float
    pressure: float


class NodeData(SQLModel, table=True):
    def generateKey():
        return "".join(random.choices(string.ascii_letters + string.digits, k=15))

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None
    slug: str | None = Field(unique=True)
    # key: str | None = Field(default=generateKey, unique=True)
