from ..database import Base

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class MonitorModel(Base):
    __tablename__ = "monitors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(25), nullable=False)

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    interval_seconds: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# class MonitorResultModel(Base):
#     __tablename__ = "monitor_result"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)

#     monitor_id: Mapped[int] = mapped_column(Integer, nullable=False)

#     status_code: Mapped[int] = mapped_column(Integer, nullable=True)

#     response_time: Mapped[float] = mapped_column(Float)

#     is_up: Mapped[bool] = mapped_column(Boolean)

#     error_message: Mapped[str] = mapped_column(String(250), nullable=True)

#     # checked_at :
