from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from backend.app.schemas.apply import ApplyRequest
from backend.app.services.applicant_service import ApplicantService

bp = Blueprint("apply", __name__)

@bp.route("/apply", methods=["POST"])
def apply():
    try:
        data = dict(request.form)
        file = request.files.get("cv")

        if not file:
            return jsonify({"error": {"code": 400, "message": "CV file is required"}}), 400

        data["cv_filename"] = file.filename

        req = ApplyRequest(**data)
        service = ApplicantService()
        resp = service.create_application(req, file)

        return jsonify(resp), 201

    except ValidationError as e:
        return jsonify({"error": {"code": 422, "message": "Validation error", "details": e.errors()}}), 422
    except ValueError as e:
        return jsonify({"error": {"code": 400, "message": str(e)}}), 400
    except Exception as e:
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500
