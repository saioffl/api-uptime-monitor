from types import NoneType

from pydantic import BaseModel


class MonitorHistoryBase(BaseModel):
    id: int
    monitor_id: int
    status_code: int | None
    response_time: float
    is_up: bool
    error_message: NoneType
    # checked_at :


class MonitorHistoryOuput(BaseModel):
    pass
