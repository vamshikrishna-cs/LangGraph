from sqlalchemy import String,DateTime, UUID, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

import uuid
import enum


from app.db.base import Base

class MeetingStatus(str, enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    needs_review = "needs_review"
    completed = "completed"
    
class Meeting(Base):    
    __tablename__ = "meetings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    audio_path:Mapped[str] = mapped_column(String, nullable=False)
    transcript: Mapped[str|None] = mapped_column(String)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    status: Mapped[MeetingStatus]=mapped_column(Enum(MeetingStatus), default=MeetingStatus.uploaded)
    decisions: Mapped[list|None]=mapped_column(JSON,nullable=True)

    
    