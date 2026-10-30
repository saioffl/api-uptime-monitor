from typing import Annotated
from ..models.history import MonitorResultModel
from ..schemas.history import MonitorHistoryBase

# from .check import post_monitor_request
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path


from ..database import get_db

router = APIRouter(prefix="/api/monitor")


@router.get("/{id}/history", response_model=list[MonitorHistoryBase])
async def post_history(
    id: Annotated[int, Path(description="Post Monitor's History")],
    db: Session = Depends(get_db),
):
    monitor_response = (
        db.query(MonitorResultModel).filter(MonitorResultModel.monitor_id == id).all()
    )
    if not monitor_response:
        raise HTTPException(status_code=404, detail="No Such Record")

    # MonitorHistoryBase.model_validate(monitor_re)
    return monitor_response
    # resp = await post_monitor_request(id=id, db=db)
    # print(resp)
