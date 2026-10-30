from typing import Annotated

# from .check import post_monitor_request
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path

from ..database import get_db

router = APIRouter(prefix="/api/monitor")


@router.post("/{id}/history")
async def post_history(
    id: Annotated[int, Path(description="Post Monitor's History")],
    db: Session = Depends(get_db),
):
    pass
