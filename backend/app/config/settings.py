from pydantic import BaseSettings, Field
from pathlib import Path
from typing import Optional

ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

class Settings(BaseSettings):
    FLASK_ENV: str = "development"
    SECRET_KEY: str = Field(...)

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str


    # Mongo
    MONGODB_URI: str = Field(...)

    FIREBASE_CREDENTIALS_JSON: Optional[str] = None
    FIREBASE_STORAGE_BUCKET: Optional[str] = None

    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024 

    DEFAULT_PAGE_SIZE: int = 25

    class Config:
        env_file = str(ENV_PATH)
        env_file_encoding = "utf-8"

settings = Settings()
