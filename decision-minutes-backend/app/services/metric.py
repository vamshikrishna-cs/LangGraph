from app.models.metric import MeetingMetric


class MetricsService:

    @staticmethod
    async def save_metrics(
        db,
        meeting_id: str,
        total_decisions: int,
        corrected_fields: int
    ):
        # Simple heuristic:
        # 2 minutes saved per decision
        minutes_saved = total_decisions * 2

        metric = MeetingMetric(
            meeting_id=meeting_id,
            total_decisions=total_decisions,
            corrected_fields=corrected_fields,
            minutes_saved=minutes_saved
        )

        db.add(metric)
        await db.commit()
