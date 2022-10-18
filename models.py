from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SensorData(Base):
    __tablename__ = "sensordata"
    id = Column(Integer, primary_key=True, index=True)
    node = Column(Integer)
    timestamp = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
