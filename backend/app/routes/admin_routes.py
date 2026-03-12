from flask import Blueprint, request, jsonify, Response, abort
from werkzeug.exceptions import HTTPException, Unauthorized
from backend.app.services.admin_service import AdminService
from backend.app.services.auth_service import AuthService

bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------------------------
# Auth Helper
# ---------------------------
def require_admin():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise Unauthorized("Missing Authorization header")

    try:
        decoded = AuthService().verify_bearer_token(auth_header)
    except ValueError as e:
        raise Unauthorized(str(e))

    if not decoded:
        raise Unauthorized("Invalid or expired token")

    return decoded


# ---------------------------
# Health Check
# ---------------------------
@bp.route("/ping", methods=["GET"])
def ping():
    require_admin()
    return jsonify({"status": "ok"}), 200


# ---------------------------
# GET /admin/applicants
# ---------------------------
@bp.route("/applicants", methods=["GET"])
def list_applicants():
    try:
        require_admin()

        # Pagination
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 25))
        except ValueError:
            return jsonify({
                "error": {"code": 400, "message": "Invalid pagination parameters"}
            }), 400

        # Filters (remove None values)
        filters = {}
        status = request.args.get("status")
        degree = request.args.get("degree")
        preferred_course = request.args.get("preferred_course")
        experience_years = request.args.get("experience_years")

        if status:
            filters["status"] = status
        if degree:
            filters["degree"] = degree
        if preferred_course:
            filters["preferred_course"] = preferred_course
        if experience_years:
            try:
                filters["experience_years"] = int(experience_years)
            except ValueError:
                return jsonify({
                    "error": {"code": 400, "message": "experience_years must be an integer"}
                }), 400

        service = AdminService()
        applicants, total = service.list_applicants(filters, page, limit)

        data = []
        for a in applicants:
            data.append({
                "applicant_id": a.applicant_id,
                "full_name": a.full_name,
                "email": a.email,
                "degree": a.degree,
                "experience_years": a.experience_years,
                "preferred_course": a.preferred_course,
                "status": a.status,
                "submitted_at": a.submitted_at.isoformat() if a.submitted_at else None,
            })

        return jsonify({
            "data": data,
            "page": page,
            "limit": limit,
            "total": total
        }), 200

    except HTTPException as e:
        return jsonify({"error": {"code": e.code, "message": e.description}}), e.code

    except Exception:
        return jsonify({
            "error": {"code": 500, "message": "Internal server error"}
        }), 500


# ---------------------------
# GET /admin/applicants/<id>
# ---------------------------
@bp.route("/applicants/<int:applicant_id>", methods=["GET"])
def get_applicant(applicant_id):
    try:
        require_admin()

        service = AdminService()
        applicant = service.get_applicant_detail(applicant_id)

        return jsonify({
            "applicant_id": applicant.applicant_id,
            "full_name": applicant.full_name,
            "email": applicant.email,
            "dob": getattr(applicant, "dob", None),
            "degree": applicant.degree,
            "experience_years": applicant.experience_years,
            "preferred_course": applicant.preferred_course,
            "location_country": getattr(applicant, "location_country", None),
            "location_state": getattr(applicant, "location_state", None),
            "status": applicant.status,
            "submitted_at": applicant.submitted_at.isoformat() if applicant.submitted_at else None,
            "cv_filename": getattr(applicant, "cv_filename", None),
            "cv_url": getattr(applicant, "cv_url", None),
            "review_comment": getattr(applicant, "review_comment", None),
        }), 200

    except ValueError as e:
        return jsonify({
            "error": {"code": 404, "message": str(e)}
        }), 404

    except HTTPException as e:
        return jsonify({"error": {"code": e.code, "message": e.description}}), e.code

    except Exception:
        return jsonify({
            "error": {"code": 500, "message": "Internal server error"}
        }), 500


# ---------------------------
# PUT /admin/applicants/<id>/status
# ---------------------------
@bp.route("/applicants/<int:applicant_id>/status", methods=["PUT"])
def update_status(applicant_id):
    try:
        require_admin()

        body = request.get_json()
        if not body or "status" not in body:
            return jsonify({
                "error": {"code": 400, "message": "Status is required"}
            }), 400

        new_status = body["status"]
        admin_comment = body.get("admin_comment")

        if not isinstance(new_status, str):
            return jsonify({
                "error": {"code": 400, "message": "Invalid status format"}
            }), 400

        service = AdminService()
        service.update_status(applicant_id, new_status, admin_comment)

        return jsonify({"message": "Status updated successfully"}), 200

    except ValueError as e:
        return jsonify({
            "error": {"code": 400, "message": str(e)}
        }), 400

    except HTTPException as e:
        return jsonify({"error": {"code": e.code, "message": e.description}}), e.code

    except Exception:
        return jsonify({
            "error": {"code": 500, "message": "Internal server error"}
        }), 500


# ---------------------------
# GET /admin/export/csv
# ---------------------------
@bp.route("/export/csv", methods=["GET"])
def export_csv():
    try:
        require_admin()

        filters = {}
        for key in ["status", "degree", "preferred_course", "experience_years"]:
            value = request.args.get(key)
            if value:
                filters[key] = value

        service = AdminService()
        csv_data = service.export_csv(filters)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=applicants.csv"
            },
        )

    except HTTPException as e:
        return jsonify({"error": {"code": e.code, "message": e.description}}), e.code

    except Exception:
        return jsonify({
            "error": {"code": 500, "message": "Internal server error"}
        }), 500