from sqlalchemy.ext.asyncio import AsyncSession
from app.models.decision import Decision


class DecisionService:

    @staticmethod
    async def save_decisions(
        db: AsyncSession,
        meeting_id: str,
        decisions: list
    ):
        for item in decisions:
            decision = Decision(
                meeting_id=meeting_id,
                decision_text=item["decision"],
                owner=item["owner"],
                deadline=item.get("deadline"),
                confidence=item["confidence"]
            )
            db.add(decision)

        await db.commit()
