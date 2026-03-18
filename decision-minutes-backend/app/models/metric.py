import uuid
from sqlalchemy import Integer, Float, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class MeetingMetric(Base):
    __tablename__ = "meeting_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    meeting_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    total_decisions: Mapped[int] = mapped_column(Integer, nullable=False)
    corrected_fields: Mapped[int] = mapped_column(Integer, nullable=False)

    minutes_saved: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
