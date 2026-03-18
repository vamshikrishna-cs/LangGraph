from pydantic import BaseModel
from typing import List 

class DecisionSchema(BaseModel):
    decision: str 
    owner: str 
    deadline: str
    confidence: float 
    
    
class ReviewStateSchema(BaseModel):
    meeting_id: str 
    audio_path: str 
    transcript: str
    decisions: List[DecisionSchema]
    blockers: list 
    overall_confidence: float
    human_approved: bool 

class ReviewRequestSchema(BaseModel):
    review_id: str 
    state: ReviewStateSchema