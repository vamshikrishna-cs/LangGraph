import boto3 
from app.core.config import settings

class S3Service:
    def __init__(self): 
        self.client=boto3.client(
            "s3", 
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        
    def upload(self,local_path:str,bucket:str,key:str)->str: 
        self.client.upload_file(local_path, bucket, key)
        return f"s3://{bucket}/{key}"