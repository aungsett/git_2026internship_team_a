# backend/app/repositories/applicant_repository.py
from typing import Optional, List, Dict, Any, Union
import importlib
from types import SimpleNamespace
from mongoengine import Document as MongoEngineDocument

# Resolve the MongoEngine Applicant Document.
# In this repo we have:
# - `backend.app.models.applicant_model.Applicant` (MongoEngine Document)
# - `backend.app.models.applicant.Applicant` (Pydantic model)
#
# Tests may monkeypatch `app.models.*`, so we try several module paths.
_CANDIDATE_MODULES = (
    "app.models.applicant_model",
    "backend.app.models.applicant_model",
    "app.models.applicant",
    "backend.app.models.applicant",
)

ApplicantDoc = None
for _mod_name in _CANDIDATE_MODULES:
    try:
        _mod = importlib.import_module(_mod_name)
    except Exception:
        continue
    # Prefer explicit Document name if available, otherwise fall back to "Applicant"
    _cand = getattr(_mod, "ApplicantDocument", None) or getattr(_mod, "Applicant", None)
    # Avoid touching MongoEngine's `.objects` manager at import time (it can require an active connection).
    if _cand is not None and isinstance(_cand, type) and issubclass(_cand, MongoEngineDocument):
        ApplicantDoc = _cand
        break

if ApplicantDoc is None:
    # As a last resort, allow non-ORM paths (unit tests) to proceed using in-memory store
    try:
        applicant_mod = importlib.import_module("backend.app.models.applicant")
        ApplicantDoc = getattr(applicant_mod, "Applicant", None)
    except Exception:
        ApplicantDoc = None

# Detect whether this ApplicantDoc is a MongoEngine Document (without touching `.objects`)
_HAS_ORM = isinstance(ApplicantDoc, type) and issubclass(ApplicantDoc, MongoEngineDocument)

# Fallback in-memory store for tests or non-DB environment
_in_memory_store: List[SimpleNamespace] = []



class ApplicantRepository:
    @staticmethod
    def get_by_email(email: str) -> Optional[Union[ApplicantDoc, SimpleNamespace]]:
        if _HAS_ORM:
            return ApplicantDoc.objects(email=email).first()
        # fallback: search in-memory
        for item in _in_memory_store:
            if item.get("email") == email:
                return item
        return None

    @staticmethod
    def get_by_applicant_id(applicant_id: int) -> Optional[Union[ApplicantDoc, SimpleNamespace]]:
        if _HAS_ORM:
            return ApplicantDoc.objects(applicant_id=applicant_id).first()
        for item in _in_memory_store:
            if item.get("applicant_id") == applicant_id:
                return item
        return None

    @staticmethod
    def create(applicant: Union[ApplicantDoc, Dict[str, Any]]):

        if _HAS_ORM:
            if isinstance(applicant, dict):
                obj = ApplicantDoc(**applicant)
                obj.save()
                return obj
            else:
                applicant.save()
                return applicant
        else:
            # in-memory path for tests
            if isinstance(applicant, dict):
                obj = dict(applicant)
            else:
                obj = dict(vars(applicant))
            _in_memory_store.append(obj)
            return obj

    @staticmethod
    def count(filters: Dict[str, Any]) -> int:
        if _HAS_ORM:
            qs = ApplicantDoc.objects(**filters)
            return int(qs.count())
        # naive in-memory count
        def matches(item):
            for k, v in filters.items():
                if v is None:
                    continue
                if getattr(item, k, None) != v:
                    return False
            return True
        return sum(1 for it in _in_memory_store if matches(it))

    @staticmethod
    def list(filters: Dict[str, Any], page: int, limit: int) -> List[Union[ApplicantDoc, SimpleNamespace]]:
        if _HAS_ORM:
            skip = (page - 1) * limit
            qs = ApplicantDoc.objects(**filters).order_by("-submitted_at").skip(skip).limit(limit)
            return list(qs)
        # in-memory naive pagination
        def matches(item):
            for k, v in filters.items():
                if v is None:
                    continue
                if getattr(item, k, None) != v:
                    return False
            return True
        filtered = [it for it in _in_memory_store if matches(it)]
        # sort by submitted_at if available (descending)
        filtered.sort(key=lambda x: getattr(x, "submitted_at", None) or 0, reverse=True)
        start = (page - 1) * limit
        return filtered[start:start + limit]

    @staticmethod
    def update_status(applicant_id: int, new_status: str, admin_comment: Optional[str] = None) -> bool:
        update_kwargs: Dict[str, Any] = {"set__status": new_status}
        if admin_comment is not None:
            update_kwargs["set__review_comment"] = admin_comment
        if _HAS_ORM:
            updated = ApplicantDoc.objects(applicant_id=applicant_id).update_one(**update_kwargs)
            return updated == 1
        for item in _in_memory_store:
            if item.get("applicant_id") == applicant_id:
                item["status"] = new_status
                if admin_comment is not None:
                    item["review_comment"] = admin_comment
                return True
        return False

    @staticmethod
    def delete(applicant_id: int) -> bool:
        """Delete an applicant by ID. Returns True if deleted, False if not found."""
        if _HAS_ORM:
            doc = ApplicantDoc.objects(applicant_id=applicant_id).first()
            if doc:
                doc.delete()
                return True
            return False
        for i, item in enumerate(_in_memory_store):
            if item.get("applicant_id") == applicant_id:
                _in_memory_store.pop(i)
                return True
        return False