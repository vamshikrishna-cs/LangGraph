from notion_client import Client
import os
from app.core.config import settings

notion = Client(auth=settings.notion_api_key)


class NotionPlanner:

    async def create_task(self, decision: str, owner: str, deadline: str):

        print("➡️ Sending to Notion:", decision)

        response = notion.pages.create(
            parent={"database_id": settings.notion_db_id},
            properties={
                "Name": {
                    "title": [
                        {"text": {"content": decision}}
                    ]
                },
                "Owner": {
                    "rich_text": [
                        {"text": {"content": owner}}
                    ]
                },
                "Deadline": {
                    "rich_text": [
                        {"text": {"content": deadline}}
                    ]
                },
            }
        )

        print("✅ Notion response:", response)