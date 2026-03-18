from app.services.planner.notion_planner import NotionPlanner
from app.core.logging import setup_logger
logger = setup_logger()

class PlannerService:

    def __init__(self):
        self.planner = NotionPlanner()

    async def create_tasks(self, decisions):

        for decision in decisions:

            await self.planner.create_task(
                decision=decision["decision"],
                owner=decision["owner"],
                deadline=decision["deadline"]
            )
        print("🔥 Creating tasks:", decisions)
        logger.info(
            "planner_tasks_created",
            extra={
                "decisions_count": len(decisions)
            }
        )