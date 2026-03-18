import boto3
import uuid 
import time 
import requests 

from app.core.config import settings

class TranscribeService:
    def __init__(self): 
        self.client=boto3.client("transcribe", region_name=settings.aws_region,aws_access_key_id=settings.aws_access_key_id,aws_secret_access_key=settings.aws_secret_access_key)
    
    def transcribe(self, file_uri:str, media_format:str)->str: 
        job_name=f"meeting-{uuid.uuid4()}"
        
        self.client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": file_uri},
            MediaFormat=media_format,
            LanguageCode="en-US",
        )
        
        while True: 
            job=self.client.get_transcription_job(TranscriptionJobName=job_name)
            
            status=job["TranscriptionJob"]["TranscriptionJobStatus"]
            
            if status == 'COMPLETED':
                transcript_uri=job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
                break 
            
            if status == 'FAILED':
                raise RuntimeError("Transcription job failed")
            
            time.sleep(5) 
            
        response=requests.get(transcript_uri)
        data=response.json()
        
        return data["results"]["transcripts"][0]["transcript"]