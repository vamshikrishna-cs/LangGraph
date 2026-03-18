from app.graph.builder import build_graph
from app.models.meeting import Meeting, MeetingStatus
from app.db.session import AsyncSessionLocal

graph=build_graph()

class WorkflowService:

    @staticmethod
    async def run_workflow(meeting_id: str, audio_path: str):

        async with AsyncSessionLocal() as db:

            meeting = await db.get(Meeting, meeting_id)

            meeting.status = "processing"
            await db.commit()

            state = {
                "meeting_id": meeting_id,
                "audio_path": audio_path,
                "transcript": None,
                "decisions": None,
                "blockers": [],
                "overall_confidence": 0.0,
                "human_approved": False
            }

            result = graph.invoke(
                state,
                config={"configurable": {"thread_id": meeting_id}}
            )

            if "__interrupt__" in result:
                meeting.transcript = result.get("transcript")
                meeting.status = "needs_review"
                meeting.decisions = result.get("decisions")
                await db.commit()
            else:
                meeting.status = "completed"

            await db.commit()