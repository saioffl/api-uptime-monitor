from pydantic import BaseModel


class MonitorStats(BaseModel):
    monitor_id: int
    total_checks: int | None
    successful_checks: int | None
    failed_checks: int | None
    uptime_percentage: int | float
    average_response_time_ms: int | float
