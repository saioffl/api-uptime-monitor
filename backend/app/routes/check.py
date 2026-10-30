import time
from typing import Annotated
import httpx
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from ..models.monitor import MonitorModel
from ..models.history import MonitorResultModel
from ..schemas.monitor import MonitorOutput, MonitorBase, MonitorCreate, MonitorHealth
from ..database import get_db


router = APIRouter(prefix="/api/monitor", tags=["checks"])


@router.get("/")
def check_monitor_request(db: Session = Depends(get_db)):
    pass


# @router.post("/{id}/check", response_model=MonitorOutput)
# async def post_monitor_request(
#     id: Annotated[int, Path(description="Check and Retrieve ID")],
#     db: Session = Depends(get_db),
# ):

#     response = db.query(MonitorModel).filter(MonitorModel.id == id).first()
#     if not response:
#         raise HTTPException(status_code=404, detail="Not a Valid ID")
#     async with httpx.AsyncClient() as client:
#         r = await client.get(response.url)
#         if not r:
#             raise httpx.RequestError(message="Error in request !")

#     # print(r.content)
#     # print(r.json())
#     print(r.status_code)
#     return response


# class MonitorHealth(BaseModel):
#     monitor_id: int
#     status_code: int
#     response_time_ms: int
#     is_up: bool
#     error_message: str
#     checked_at: datetime.datetime


@router.post("/{id}/check", response_model=MonitorHealth)
async def post_monitor_request(
    id: Annotated[int, Path(description="Post Monitor Request")],
    db: Session = Depends(get_db),
):
    start_time = time.perf_counter()
    db_response = db.query(MonitorModel).filter(MonitorModel.id == id).first()
    if not db_response:
        raise HTTPException(status_code=404, detail="Not a valid db id")
    async with httpx.AsyncClient() as client:
        response = await client.get(db_response.url)
        if not response:
            raise httpx.TimeoutException(message="Timeout !")
    end_time = time.perf_counter()
    total_time = (end_time - start_time) * 1000

    print(response)

    history = MonitorResultModel(
        monitor_id=id,
        status_code=response.status_code,
        response_time_ms=total_time,
        is_up=200 <= response.status_code < 400,
        error_message=None,
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    print(history)
    return MonitorHealth(
        monitor_id=id,
        status_code=response.status_code,
        response_time_ms=total_time,
        is_up=200 <= response.status_code < 400,
        error_message=None,
    )
