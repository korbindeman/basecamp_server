from typing import List
from sqlmodel import Field, SQLModel, Relationship


class NodeDataBase(SQLModel):
    name: str
    description: str | None


class NodeData(NodeDataBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    key: str | None = Field(default=None, unique=True)

    sensordata: List["SensorData"] = Relationship(back_populates="node")


class NodeDataRead(NodeDataBase):
    id: int


class NodeDataReadAfterCreate(NodeDataRead):
    key: str


class NodeDataCreate(NodeDataBase):
    pass


class SensorDataBase(SQLModel):
    timestamp: int
    temperature: float
    humidity: float
    pressure: float


class SensorData(SensorDataBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    node_id: int | None = Field(default=None, foreign_key="nodedata.id")
    node: NodeData = Relationship(back_populates="sensordata")


class SensorDataCreate(SensorDataBase):
    key: str


class SensorDataRead(SensorDataBase):
    id: int
