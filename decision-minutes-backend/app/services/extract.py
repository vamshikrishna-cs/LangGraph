from groq import Groq 
from app.core.config import settings 
import json 

class ExtractionService: 
    def __init__(self): 
        self.client=Groq(api_key=settings.groq_api_key) 
        
    def extract(self,transcript:str): 
        prompt=f"""
You are an AI meeting assistant. 

Extract: 
- Decisions 
- Owners 
- Deadlines 
- Blockers

Return strict JSON in the format:
{{
    "decisions":[
        {{
            "decision": "...",
            "owner": "...",
            "deadline": "...",
            "confidence":0.0
        }}
    ],
    "blockers":[],
    "overall_confidence":0.0
}}

Transcript:
{transcript}
"""
        response=self.client.chat.completions.create( 
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}],
            temperature=0
            )
        content=response.choices[0].message.content
        return json.loads(content)