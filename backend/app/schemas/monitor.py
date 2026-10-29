import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl


class MonitorBase(BaseModel):
    id: int
    name: str
    url: HttpUrl
    interval_seconds: int
    is_active: bool
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


class MonitorCreate(BaseModel):
    name: str
    url: HttpUrl
    interval_seconds: int


class MonitorOutput(BaseModel):
    name: str
    is_active: bool
