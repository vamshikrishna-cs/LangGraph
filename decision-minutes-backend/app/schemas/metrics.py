from pydantic import BaseModel
from uuid import UUID

class MetricsSummary(BaseModel): 
    total_meetings: int
    total_decisions: int
    minutes_saved: float 
    
class MeetingMetricsResponse(BaseModel):
    meeting_id: UUID
    total_decisions: int
    corrected_fields: int
    minutes_saved: float