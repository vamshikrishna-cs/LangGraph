from app.services.transcribe import TranscribeService
from app.services.s3 import S3Service
from app.core.config import settings
from app.core.logging import setup_logger
logger = setup_logger()
def asr_node(state): 
    s3=S3Service() 
    transcriber=TranscribeService()
    
    s3_uri=s3.upload(
        state["audio_path"],
        settings.s3_bucket,
        f"meetings/{state['meeting_id']}.wav"
    )
    
    transcript=transcriber.transcribe(s3_uri,"wav")
    logger.info("transcription_completed", extra={"meeting_id": state["meeting_id"]})
    state["transcript"]=transcript
    return state