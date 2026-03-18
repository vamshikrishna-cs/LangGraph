from abc import ABC, abstractmethod


class BasePlanner(ABC):

    @abstractmethod
    async def create_task(
        self,
        decision: str,
        owner: str,
        deadline: str
    ):
        pass