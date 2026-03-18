from app.services.extract import ExtractionService
from app.core.logging import setup_logger

logger = setup_logger()



def extract_node(state):
    extractor=ExtractionService()
    
    result=extractor.extract(state["transcript"])
    
    logger.info(
        "decisions_extracted",
        extra={
            "meeting_id": state["meeting_id"],
            "decisions_count": len(result['decisions'])
        }
    )
    
    state['decisions']=result['decisions']
    state['blockers']=result.get('blockers')
    state['overall_confidence']=result['overall_confidence']
    
    return state