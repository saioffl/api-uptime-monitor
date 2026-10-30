import datetime
from types import NoneType
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


class MonitorHealth(BaseModel):
    monitor_id: int
    status_code: int
    response_time_ms: float
    is_up: bool
    error_message: NoneType
    # checked_at: datetime.datetime


class MonitorOutput(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
