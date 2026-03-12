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
        # Support both:
        # - JSON requests (e.g., API clients/tests)
        # - multipart/form-data from the HTML form (includes CV upload)
        body = request.get_json(silent=True)
        is_multipart = bool(request.form) or bool(request.files)

        data_in = None
        file_obj = None

        if body:
            data_in = dict(body)
        elif is_multipart:
            file_obj = request.files.get("cv") or request.files.get("file")
            if not file_obj:
                return jsonify({"error": {"code": 400, "message": "CV file is required"}}), 400

            form = request.form
            # Accept both snake_case and the field names used by `frontend/application_form.html`
            data_in = {
                "full_name": form.get("full_name") or form.get("fullName"),
                "dob": form.get("dob"),
                "email": form.get("email"),
                "degree": form.get("degree"),
                "experience_years": form.get("experience_years") or form.get("experience"),
                "preferred_course": form.get("preferred_course") or form.get("course"),
                "location_country": form.get("location_country") or form.get("country"),
                "location_state": form.get("location_state") or form.get("state"),
                "comments": form.get("comments"),
                "cv_filename": getattr(file_obj, "filename", None),
                # werkzeug FileStorage exposes content_length sometimes; fall back to 0 to skip size validation if unknown
                "cv_size": getattr(file_obj, "content_length", None) or 0,
            }
        else:
            return jsonify({"error": {"code": 400, "message": "Request body is required"}}), 400

        payload = ApplySchema(**data_in)

        # convert pydantic model -> plain dict (compatible with v2 and v1)
        if hasattr(payload, "model_dump"):
            data = payload.model_dump()
        elif hasattr(payload, "dict"):
            data = payload.dict()
        else:
            data = dict(payload)

        service = ApplicantService()
        if file_obj is None:
            # JSON-only submission (no CV upload). Keep backwards compatibility.
            return jsonify({
                "error": {"code": 400, "message": "CV upload is required for applications"}
            }), 400

        created = service.create_applicant(data, file_obj)

        return jsonify({
            "message": "Application submitted successfully",
            "application_id": created.applicant_id
        }), 201

    except ValidationError as e:
        details = _sanitize_pydantic_errors(e.errors())
        return jsonify({
            "error": {"code": 400, "message": "Validation error", "details": details}
        }), 400

    except ValueError as e:
        # Domain errors from the service layer (e.g., duplicate email)
        return jsonify({
            "error": {"code": 400, "message": str(e)}
        }), 400

    except Exception as e:
        # Temporary: surface exact error in logs while developing
        print("ERROR in create_applicant:", repr(e))
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500