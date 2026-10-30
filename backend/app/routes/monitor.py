from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Path
from ..database import get_db
from ..models.monitor import MonitorModel
from ..schemas.monitor import MonitorBase, MonitorOutput, MonitorCreate

router = APIRouter(prefix="/api/monitor", tags=["monitor"])


@router.get(
    "/",
    response_model=list[MonitorOutput],
)
def get_api(db: Session = Depends(get_db)):
    resp = db.query(MonitorModel).all()

    if not resp:
        raise HTTPException(status_code=404, detail="API not found")
    print([obj.__dict__ for obj in resp])
    return resp


@router.get("/{id}", response_model=MonitorOutput)
def get_specific_api(
    id: Annotated[int, Path(description="Get Specific API")],
    db: Session = Depends(get_db),
):

    resp = db.query(MonitorModel).filter(MonitorModel.id == id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Response is None")
    return resp


@router.post("/", response_model=MonitorOutput)
def post_api(payload: MonitorCreate, db: Session = Depends(get_db)):
    resp = MonitorModel(**payload.model_dump())
    if not resp:
        raise HTTPException(status_code=404, detail="Response is None")
    db.add(resp)
    db.commit()
    db.refresh(resp)

    return resp


@router.put("/{id}", response_model=MonitorBase)
def update_api(
    id: Annotated[int, Path(description="Update API")],
    payload: MonitorBase,
    db: Session = Depends(get_db),
):
    resp = db.query(MonitorModel).filter(MonitorModel.id == id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Resp Is None")
    for key, value in payload.model_dump().items():
        setattr(resp, key, value)

    # db.add(resp)
    db.commit()
    db.refresh(resp)

    return resp


@router.delete("/{id}")
def delete_api(
    id: Annotated[int, Path(description="Delete API")], db: Session = Depends(get_db)
):

    resp = db.query(MonitorModel).filter(MonitorModel.id == id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Response Input is Empty !")
    saved_response = MonitorBase.model_validate(resp)
    db.delete(resp)
    db.commit()

    return {"message": f"Deleted {saved_response}Successfully"}
