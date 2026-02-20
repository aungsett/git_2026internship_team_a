# backend/app/services/storage_service.py
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

        # Build Cloudinary upload; keeping it simple: upload the raw file to folder
        # You can set public_id or use applicant_id as part of public_id if you want naming
        public_id = None
        if isinstance(applicant_id_or_filename, int):
            # make a sensible public id using applicant id + original name (without spaces)
            orig = getattr(file_obj, "filename", filename)
            safe_name = orig.replace(" ", "_")
            public_id = f"ats/cv/{applicant_id_or_filename}_{safe_name}"

        upload_kwargs = {"resource_type": "raw"}
        if public_id:
            # cloudinary expects public_id without folder when folder param used; we'll pass folder via public_id prefix
            # to keep things simple, pass folder and let cloudinary create unique names
            upload_kwargs["folder"] = "ats/cv"
            # we still won't pass public_id to avoid collisions; optional: pass public_id=...
            # upload_kwargs["public_id"] = f"{applicant_id_or_filename}_{safe_name}"

        # cloudinary.uploader.upload accepts file-like object or path
        res = cloudinary.uploader.upload(file_obj, **upload_kwargs)
        url = res.get("secure_url")
        if not url:
            raise RuntimeError("Cloudinary did not return secure_url")
        return url
