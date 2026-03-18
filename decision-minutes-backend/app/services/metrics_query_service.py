from sqlalchemy import select, func 
from app.models.metric import MeetingMetric

class MetricsQueryService:
    
    
    @staticmethod
    async def get_summary(db): 
        total_meetings=await db.scalar(select(func.count(MeetingMetric.meeting_id)))
        total_decisions=await db.scalar(select(func.sum(MeetingMetric.total_decisions)))
        minutes_saved=await db.scalar(select(func.sum(MeetingMetric.minutes_saved)))
        
        return {
            "total_meetings": total_meetings or 0,
            "total_decisions": total_decisions or 0,
            "minutes_saved": minutes_saved or 0
        }
        
    @staticmethod
    async def get_meeting_metrics(db): 
        result=await db.execute(
            select(
                MeetingMetric.meeting_id,
                MeetingMetric.total_decisions,
                MeetingMetric.corrected_fields,
                MeetingMetric.minutes_saved
            )
        )
        
        return result.all()