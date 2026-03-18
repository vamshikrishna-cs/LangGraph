from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.metrics_query_service import MetricsQueryService

router=APIRouter(prefix="/metrics",tags=["metrics"])

@router.get("/summary")
async def metrics_summary(db:AsyncSession=Depends(get_db)):
    summary=await MetricsQueryService.get_summary(db)
    return summary

@router.get("/meetings")
async def meeting_metrics(db:AsyncSession=Depends(get_db)):
    rows=await MetricsQueryService.get_meeting_metrics(db)
    
    return [
        {
            "meeting_id": r.meeting_id,
            "total_decisions": r.total_decisions,
            "corrected_fields": r.corrected_fields,
            "minutes_saved": r.minutes_saved
        }
        for r in rows
    ]
