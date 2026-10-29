from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path
from ..database import get_db
from ..models.api import APIModel
from ..schemas.api import APIBase, APIOutput

router = APIRouter(prefix="/api", tags=["api"])

message = {"WELCOME DAWG"}


@router.get(
    "/",
    response_model=list[APIOutput],
)
def get_api(db: Session = Depends(get_db)):
    resp = db.query(APIModel).all()
    print([obj.__dict__ for obj in resp])
    return resp


@router.get("/{id}", response_model=APIOutput)
def get_specific_api(
    id: Annotated[int, Path(description="Get Specific API")],
    db: Session = Depends(get_db),
):

    resp = db.query(APIModel).filter(APIModel.id == id).first()
    return resp


@router.post("/")
def post_api(payload: APIBase, db: Session = Depends(get_db)):
    resp = APIModel(**payload.model_dump())
    db.add(resp)
    db.commit()
    db.refresh(resp)

    return resp


@router.put("/{id}")
def update_api(
    id: Annotated[int, Path(description="Update API")],
    payload: APIBase,
    db: Session = Depends(get_db),
):
    resp = db.query(APIModel).filter(APIModel.id == id).first()
    for key, value in payload.model_dump().items():
        setattr(resp, key, value)

    db.add(resp)
    db.commit()
    db.refresh(resp)

    return resp


@router.delete("/{id}")
def delete_api(
    id: Annotated[int, Path(description="Delete API")], db: Session = Depends(get_db)
):

    resp = db.query(APIModel).filter(APIModel.id == id).first()
    saved_response = APIBase.model_validate(resp)
    db.delete(resp)
    db.commit()

    return {"message": f"Deleted {saved_response}Successfully"}
