from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Path
from ..database import get_db
from ..models.user import UserModel
from ..schemas.user import UserBase, UserOutput

router = APIRouter(prefix="/api", tags=["api"])


@router.get(
    "/user",
    response_model=list[UserOutput],
)
def get_api(db: Session = Depends(get_db)):
    resp = db.query(UserModel).all()

    if resp is None:
        raise HTTPException(status_code=404, detail="API not found")
    print([obj.__dict__ for obj in resp])
    return resp


@router.get("user/{id}", response_model=UserOutput)
def get_specific_api(
    id: Annotated[int, Path(description="Get Specific API")],
    db: Session = Depends(get_db),
):

    resp = db.query(UserModel).filter(UserModel.id == id).first()
    return resp


@router.post("user/")
def post_api(payload: UserBase, db: Session = Depends(get_db)):
    resp = UserModel(**payload.model_dump())
    db.add(resp)
    db.commit()
    db.refresh(resp)

    return resp


@router.put("user/{id}")
def update_api(
    id: Annotated[int, Path(description="Update API")],
    payload: UserBase,
    db: Session = Depends(get_db),
):
    resp = db.query(UserModel).filter(UserModel.id == id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Resp Is None")
    for key, value in payload.model_dump().items():
        setattr(resp, key, value)

    db.add(resp)
    db.commit()
    db.refresh(resp)

    return resp


@router.delete("user/{id}")
def delete_api(
    id: Annotated[int, Path(description="Delete API")], db: Session = Depends(get_db)
):

    resp = db.query(UserModel).filter(UserModel.id == id).first()
    saved_response = UserBase.model_validate(resp)
    db.delete(resp)
    db.commit()

    return {"message": f"Deleted {saved_response}Successfully"}
