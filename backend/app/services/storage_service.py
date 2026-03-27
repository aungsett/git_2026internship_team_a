# backend/app/services/storage_service.py
from pathlib import Path
from typing import Union
from backend.app.config.settings import settings
from backend.app.utils.validators import validate_cv_filename
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=getattr(settings, "CLOUDINARY_CLOUD_NAME", None),
    api_key=getattr(settings, "CLOUDINARY_API_KEY", None),
    api_secret=getattr(settings, "CLOUDINARY_API_SECRET", None),
    secure=True,
)


class StorageService:
    """
    Upload CVs to Cloudinary. upload_cv accepts either:
      - (file_obj, filename_str)
      - (file_obj, applicant_id_int)
    Tests call upload_cv(file, 60001) so we support that.
    """

    def upload_cv(self, file_obj, applicant_id_or_filename: Union[int, str]) -> str:
        # determine the filename to validate
        if isinstance(applicant_id_or_filename, int):
            # caller passed applicant_id (tests do this). Use file_obj.filename for validation.
            filename = getattr(file_obj, "filename", None)
            if not filename:
                raise ValueError("Uploaded file must have a filename")
        else:
            # caller passed a filename string
            filename = str(applicant_id_or_filename)

        # validate extension, raises ValueError on invalid extension
        validate_cv_filename(filename)

        # Keep original basename + extension in Cloudinary so downloads preserve type and name.
        # We isolate files by applicant id folder to avoid filename collisions.
        original_name = Path(filename).name
        stem = Path(original_name).stem.replace(" ", "_")
        ext = Path(original_name).suffix.lower().lstrip(".")

        upload_kwargs = {
            "resource_type": "raw",
            "use_filename": True,
            "unique_filename": False,
            "overwrite": True,
        }
        if isinstance(applicant_id_or_filename, int):
            upload_kwargs["folder"] = f"ats/cv/{applicant_id_or_filename}"
            upload_kwargs["public_id"] = stem
        else:
            upload_kwargs["folder"] = "ats/cv"
            upload_kwargs["public_id"] = stem

        if ext:
            upload_kwargs["format"] = ext

        # cloudinary.uploader.upload accepts file-like object or path
        res = cloudinary.uploader.upload(file_obj, **upload_kwargs)
        url = res.get("secure_url")
        if not url:
            raise RuntimeError("Cloudinary did not return secure_url")
        return url
