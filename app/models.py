from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint

from sqlmodel import Field, SQLModel


class NodesBase(SQLModel):
    name: str = Field(unique=True, max_length=20)
    description: str = Field(max_length=100)


class Nodes(NodesBase, table=True):
    __table_args__ = (UniqueConstraint("name", "key"),)
    id: int | None = Field(default=None, primary_key=True)
    key: str


class NodesCreate(NodesBase):
    pass


class NodesRead(NodesBase):
    id: int


class SensorDataBase(SQLModel):
    timestamp: int
    temperature: float
    humidity: float
    pressure: float


class SensorData(SensorDataBase, table=True):
    __table_args__ = (
        PrimaryKeyConstraint("node_id", "timestamp", name="sensordata_pk"),
    )

    node_id: int


class SensorDataCreate(SensorDataBase):
    pass


class SensorDataRead(SensorDataBase):
    node_id: int
