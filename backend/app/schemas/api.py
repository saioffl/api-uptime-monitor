import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class APIBase(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class APIOutput(BaseModel):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
