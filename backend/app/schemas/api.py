import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class UserOutput(BaseModel):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
