from flask import Blueprint, request, jsonify, Response
from backend.app.services.admin_service import AdminService
from backend.app.services.auth_service import AuthService

bp = Blueprint("admin", __name__, url_prefix="/admin")


def require_admin():
    auth_header = request.headers.get("Authorization")
    decoded = AuthService().verify_bearer_token(auth_header)
    return decoded


@bp.route("/ping", methods=["GET"])
def ping():
    require_admin()
    return jsonify({"status": "ok"}), 200


@bp.route("/applicants", methods=["GET"])
def list_applicants():
    try:
        require_admin()

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 25))

        filters = {
            "status": request.args.get("status"),
            "degree": request.args.get("degree"),
            "preferred_course": request.args.get("preferred_course"),
            "experience_years": request.args.get("experience_years"),
        }

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
                "submitted_at": a.submitted_at,
            })

        return jsonify({
            "data": data,
            "page": page,
            "limit": limit,
            "total": total
        }), 200

    except ValueError as e:
        return jsonify({"error": {"code": 400, "message": str(e)}}), 400
    except Exception:
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500


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
            "degree": applicant.degree,
            "experience_years": applicant.experience_years,
            "preferred_course": applicant.preferred_course,
            "status": applicant.status,
            "submitted_at": applicant.submitted_at,
            "cv_url": applicant.cv_url,
        }), 200

    except ValueError as e:
        return jsonify({"error": {"code": 404, "message": str(e)}}), 404
    except Exception:
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500


@bp.route("/applicants/<int:applicant_id>/status", methods=["PUT"])
def update_status(applicant_id):
    try:
        require_admin()

        body = request.get_json()
        if not body or "status" not in body:
            return jsonify({"error": {"code": 400, "message": "Status is required"}}), 400

        new_status = body["status"]

        service = AdminService()
        service.update_status(applicant_id, new_status)

        return jsonify({"message": "Status updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": {"code": 400, "message": str(e)}}), 400
    except Exception:
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500


@bp.route("/export/csv", methods=["GET"])
def export_csv():
    try:
        require_admin()

        filters = {
            "status": request.args.get("status"),
            "degree": request.args.get("degree"),
            "preferred_course": request.args.get("preferred_course"),
            "experience_years": request.args.get("experience_years"),
        }

        service = AdminService()
        csv_data = service.export_csv(filters)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=applicants.csv"},
        )

    except Exception:
        return jsonify({"error": {"code": 500, "message": "Internal server error"}}), 500
