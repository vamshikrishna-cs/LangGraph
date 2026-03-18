from asyncio.log import logger

from fastapi import APIRouter, UploadFile, File, Depends, Body, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import shutil 
from pathlib import Path

from app.db.session import get_db
from app.models.meeting import Meeting
from app.core.config import settings
from app.graph.builder import build_graph

from app.services.decision import DecisionService
from app.services.metric import MetricsService
from app.services.planner_service import PlannerService
from app.services.workflow_service import WorkflowService

from app.schemas.review import ReviewRequestSchema

router=APIRouter()
graph=build_graph()

UPLOAD_DIR=Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/meetings")
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db:AsyncSession = Depends(get_db),
): 
    file_path=UPLOAD_DIR / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    meeting=Meeting(audio_path=str(file_path))
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    
    logger.info("meeting_uploaded",extra={"meeting_id": meeting.id, "audio_path": str(file_path)})

    background_tasks.add_task(WorkflowService.run_workflow, str(meeting.id), str(file_path))

    return {
        "meeting_id": meeting.id,
        "status": "processing"
    }
    
@router.post("/meetings/review")
async def submit_review(
    payload: ReviewRequestSchema,
    db: AsyncSession = Depends(get_db)
):

    review_id = payload.review_id
    updated_state = payload.state.dict()

    updated_state["human_approved"] = True
    updated_state["overall_confidence"] = 1.0

    graph.update_state(
        {"configurable": {"thread_id": review_id}},
        updated_state
    )

    result = graph.invoke(
        None,
        config={"configurable": {"thread_id": review_id}}
    )
    original = graph.get_state(
        {"configurable": {"thread_id": review_id}}
    ).values

    corrected = payload.state.dict()

    corrected_fields = 0

    for i, decision in enumerate(corrected["decisions"]):
        if decision["owner"] != original["decisions"][i]["owner"]:
            corrected_fields += 1

        if decision["deadline"] != original["decisions"][i]["deadline"]:
            corrected_fields += 1
            
    logger.info(
        "human_review_completed",
        extra={
            "decisions_count": len(corrected["decisions"]),
            "meeting_id": updated_state["meeting_id"],
            "corrected_fields": corrected_fields
        }
    )


    # Persist approved decisions
    await DecisionService.save_decisions(
        db=db,
        meeting_id=result["meeting_id"],
        decisions=result["decisions"]
    )

    await MetricsService.save_metrics(
        db=db,
        meeting_id=result["meeting_id"],
        total_decisions=len(result["decisions"]),
        corrected_fields=corrected_fields
    )
    
    try:
        planner = PlannerService()
        corrected=payload.state.dict()
        
        await planner.create_tasks(corrected["decisions"])
        print("🔥 Planner called")
    except Exception as e:
        logger.error("Planner task creation failed", exc_info=e)

    return {
        "status": "completed",
        "result": result
    }
    
@router.get("/meetings/{meeting_id}")
async def get_meeting_status(
    meeting_id: str,
    db: AsyncSession = Depends(get_db)
):

    meeting = await db.get(Meeting, meeting_id)

    if not meeting:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "meeting_id": meeting.id,
        "status": meeting.status,
        "state": {
            "meeting_id": meeting.id,
            "audio_path": meeting.audio_path,
            "transcript": meeting.transcript,
            "decisions": meeting.decisions or [],
            "blockers": [],
        }
    }