# backend/app/repositories/applicant_repository.py
from typing import Optional, List, Dict, Any, Union
import importlib
from types import SimpleNamespace

# Try to import the module path that unit tests may patch ('app.models.applicant'),
# otherwise fall back to the real package path used by the running app.
try:
    applicant_mod = importlib.import_module("app.models.applicant")
except Exception:
    applicant_mod = importlib.import_module("backend.app.models.applicant")

# Prefer an explicit Document class name if available
ApplicantDoc = getattr(applicant_mod, "ApplicantDocument", None) or getattr(applicant_mod, "Applicant", None)
if ApplicantDoc is None:
    raise ImportError("Could not find Applicant class in app.models.applicant or backend.app.models.applicant")

# Detect whether this ApplicantDoc is a MongoEngine Document (has .objects)
_HAS_ORM = hasattr(ApplicantDoc, "objects")

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
    def update_status(applicant_id: int, new_status: str) -> bool:
        if _HAS_ORM:
            updated = ApplicantDoc.objects(applicant_id=applicant_id).update_one(set__status=new_status)
            return updated == 1
        for item in _in_memory_store:
            if item.get("applicant_id") == applicant_id:
                item["status"] = new_status
                return True
        return False