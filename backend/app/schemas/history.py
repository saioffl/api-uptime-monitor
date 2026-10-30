from types import NoneType

from pydantic import BaseModel, ConfigDict


class MonitorHistoryBase(BaseModel):
    id: int
    monitor_id: int
    status_code: int | None
    response_time_ms: float
    is_up: bool
    error_message: str | None
    model_config = ConfigDict(from_attributes=True)
    # checked_at :


class MonitorHistoryOuput(BaseModel):
    pass
