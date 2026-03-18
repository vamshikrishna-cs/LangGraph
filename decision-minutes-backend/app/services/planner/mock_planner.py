from app.services.planner.base import BasePlanner
from app.core.logging import setup_logger
logger = setup_logger()

class MockPlanner(BasePlanner):

    async def create_task(
        self,
        decision: str,
        owner: str,
        deadline: str
    ):
        # Simulate task creation
        logger.info(
            "task_created",
            extra={
                "decision": decision,
                "owner": owner,
                "deadline": deadline
            }
        )