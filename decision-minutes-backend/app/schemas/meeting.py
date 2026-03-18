from pydantic import BaseModel
from uuid import UUID

class MeetingCreate(BaseModel):
    pass 

class MeetingResponse(BaseModel): 
    id: UUID
    audio_path: str
    
    class Config:
        from_attributes = True
        