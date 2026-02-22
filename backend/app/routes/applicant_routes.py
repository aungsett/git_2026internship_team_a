from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from backend.app.models.applicant import Applicant
from backend.app.services.applicant_service import ApplicantService

applicant_bp = Blueprint("applicant", __name__, url_prefix="/applicants")


@applicant_bp.route("", methods=["POST"])
def create_applicant():
    try:
        body = request.get_json(silent=True)  # ✅ FIX HERE

        if not body:
            return jsonify({
                "error": {"code": 400, "message": "Request body is required"}
            }), 400

        applicant = Applicant(**body)

        service = ApplicantService()
        created = service.create_applicant(applicant)

        return jsonify({
            "message": "Application submitted successfully",
            "application_id": created.applicant_id
        }), 201

    except ValidationError as e:
        return jsonify({
            "error": {"code": 400, "message": e.errors()}
        }), 400

    except Exception:
        return jsonify({
            "error": {"code": 500, "message": "Internal server error"}
        }), 500