from typing import Annotated
from ..database import get_db
from ..schemas.stats import MonitorStats
from ..models.history import MonitorResultModel
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/monitor", tags=["stats"])


@router.get("/{id}/stats", response_model=MonitorStats)
def get_monitor_stats(
    id: Annotated[int, Path(description="Get Statistic of Monitor")],
    db: Session = Depends(get_db),
):
    response = (
        db.query(MonitorResultModel).filter(MonitorResultModel.monitor_id == id).all()
    )
    if not response:
        raise HTTPException(status_code=404, detail="No such Monitor ID in DB")

    total_checks = len(response)

    success_status_codes = 0
    failure_status_codes = 0
    response_times = 0

    # Better Logic to find is_up dawg !
    for isup in response:
        response_times += isup.response_time_ms
        if isup.is_up:
            success_status_codes += 1
        else:
            failure_status_codes += 1

    # Bad Logic, check above for directly retreiving is_up status !!
    #     for value in response:
    #         response_times += value.response_time_ms
    #         if value.status_code >= 200 and value.status_code < 400:
    #             success_status_code_list.append(value.status_code)
    #         else:
    #             failure_status_code_list.append(value.status_code)

    uptime_percentage = round(success_status_codes / total_checks, 2)

    average_response_time_ms = round(response_times / total_checks, 2)

    return MonitorStats(
        monitor_id=id,
        total_checks=total_checks,
        successful_checks=success_status_codes,
        failed_checks=failure_status_codes,
        uptime_percentage=uptime_percentage,
        average_response_time_ms=average_response_time_ms,
    )


# Example Response

# {
#   "monitor_id": 4,
#   "total_checks": 100,
#   "successful_checks": 98,
#   "failed_checks": 2,
#   "uptime_percentage": 98.0,
#   "average_response_time_ms": 142.5
# }
