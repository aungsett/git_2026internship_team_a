# backend/app/routes/applicant_routes.py
from importlib import import_module
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from backend.app.services.applicant_service import ApplicantService

applicant_bp = Blueprint("applicant", __name__, url_prefix="/applicants")

# Try several likely schema names so this file is tolerant to minor naming differences.
_apply_module = import_module("backend.app.schemas.apply")
_APPLY_CANDIDATES = ("Apply", "ApplyRequest", "ApplySchema", "ApplyModel", "ApplyIn")
ApplySchema = None
for _n in _APPLY_CANDIDATES:
    if hasattr(_apply_module, _n):
        ApplySchema = getattr(_apply_module, _n)
        break

if ApplySchema is None:
    raise ImportError(
        "No request schema class found in backend.app.schemas.apply. "
        f"Tried names: {_APPLY_CANDIDATES}"
    )


def _sanitize_pydantic_errors(errors_list):
    out = []
    for e in errors_list:
        loc = e.get("loc")
        msg = e.get("msg") or e.get("message") or ""
        out.append({
            "loc": list(loc) if isinstance(loc, (tuple, list)) else loc,
            "msg": str(msg),
        })
    return out


@applicant_bp.route("", methods=["POST"])
def create_applicant():
    try:
        body = request.get_json(silent=True)
        if not body:
            return jsonify({"error": {"code": 400, "message": "Request body is required"}}), 400

        payload = ApplySchema(**body)

        # convert pydantic model -> plain dict (compatible with v2 and v1)
        if hasattr(payload, "model_dump"):
            data = payload.model_dump()
        elif hasattr(payload, "dict"):
            data = payload.dict()
        else:
            data = dict(payload)

        service = ApplicantService()
        created = service.create_applicant(data)

        return jsonify({
            "message": "Application submitted successfully",
            "application_id": created.applicant_id
        }), 201

    except ValidationError as e:
        details = _sanitize_pydantic_errors(e.errors())
        return jsonify({
            "error": {"code": 400, "message": "Validation error", "details": details}
        }), 400

    except Exception:
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500