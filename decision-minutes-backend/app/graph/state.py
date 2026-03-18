from typing import TypedDict, List, Optional

class Decision(TypedDict): 
    decision: str 
    owner: str 
    deadline: str 
    confidence: float
    
class GraphState(TypedDict): 
    meeting_id: int 
    audio_path: str
    transcript: Optional[str]
    decisions: Optional[List[Decision]]
    blockers: Optional[list]
    overall_confidence: Optional[float]
    human_approved: bool