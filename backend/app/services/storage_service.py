from typing import Protocol
from backend.app.utils.validators import validate_cv_filename
from backend.app.config.settings import settings
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

class StorageService:
    def upload_cv(self, file_obj, filename: str) -> str:
        validate_cv_filename(filename)

        res = cloudinary.uploader.upload(
            file_obj,
            folder="ats/cv",
            resource_type="raw",
        )
        return res["secure_url"]
