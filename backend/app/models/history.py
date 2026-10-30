from ..database import Base

# from datetime import datetime
from sqlalchemy import Float, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class MonitorResultModel(Base):
    __tablename__ = "monitor_result"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    monitor_id: Mapped[int] = mapped_column(Integer, nullable=False)

    status_code: Mapped[int] = mapped_column(Integer, nullable=True)

    response_time_ms: Mapped[float] = mapped_column(Float)

    is_up: Mapped[bool] = mapped_column(Boolean)

    error_message: Mapped[str | None] = mapped_column(String(250), nullable=True)

    # checked_at :
