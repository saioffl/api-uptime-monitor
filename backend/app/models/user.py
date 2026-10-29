from sqlalchemy import Date, DateTime, Integer, String

from ..database import Base
from sqlalchemy.orm import mapped_column, Mapped


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(25), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(25), nullable=False)
    created_at: Mapped[Date] = mapped_column(DateTime, nullable=False)
