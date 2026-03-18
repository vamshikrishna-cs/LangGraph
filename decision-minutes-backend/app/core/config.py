from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str
    database_url: str
    aws_region: str
    groq_api_key: str
    s3_bucket: str
    aws_access_key_id: str
    aws_secret_access_key: str
    notion_api_key: str
    notion_db_id: str

    class Config:
        env_file = ".env"

settings = Settings()
