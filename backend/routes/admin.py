from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from models import db

from models.user import User
from models.incident import Incident


# =====================================================
# Blueprint
# =====================================================

admin_bp = Blueprint(
    "admin",
    __name__
)


# =====================================================
# Official Authentication
#
# Only Officials can access Admin APIs
# =====================================================

def official_required(function):

    @wraps(function)

    @jwt_required()

    def wrapper(*args, **kwargs):

        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user is None:

            return jsonify({

                "success": False,

                "message": "User not found."

            }), 404

        if user.role != "Official":

            return jsonify({

                "success": False,

                "message": "Access Denied."

            }), 403

        return function(*args, **kwargs)

    return wrapper


# =====================================================
# Dashboard Statistics Helper
# =====================================================

def dashboard_statistics():

    total_reports = Incident.query.count()

    pending_reports = Incident.query.filter_by(
        status="Pending"
    ).count()

    approved_reports = Incident.query.filter_by(
        status="Approved"
    ).count()

    rejected_reports = Incident.query.filter_by(
        status="Rejected"
    ).count()

    high_risk = Incident.query.filter(
        Incident.severity.in_(
            ["High", "Very High"]
        )
    ).count()

    return {

        "totalReports": total_reports,

        "pendingReports": pending_reports,

        "approvedReports": approved_reports,

        "rejectedReports": rejected_reports,

        "highRiskReports": high_risk

    }


# =====================================================
# Helper Function
#
# Convert Incident Object to JSON
# =====================================================

def incident_to_dict(report):

    return {

        "id": report.id,

        "title": report.title,

        "description": report.description,

        "location": report.location,

        "district": report.district,

        "severity": report.severity,

        "status": report.status,

        "image": report.image,

        "video": report.video,

        "admin_remark": report.admin_remark,

        "user_id": report.user_id,

        "created_at": report.created_at,

        "updated_at": report.updated_at

    }


# =====================================================
# Helper Function
#
# Fetch Incident
# =====================================================

def get_incident_or_404(incident_id):

    incident = Incident.query.get(incident_id)

    if incident is None:

        return None

    return incident
# =====================================================
# Admin Dashboard Statistics
#
# GET /api/admin/dashboard
# =====================================================

@admin_bp.route("/dashboard", methods=["GET"])
@official_required
def dashboard():

    return jsonify({

        "success": True,

        "statistics": dashboard_statistics()

    }), 200


# =====================================================
# Get All Incident Reports
#
# GET /api/admin/incidents
# =====================================================

@admin_bp.route("/incidents", methods=["GET"])
@official_required
def get_all_incidents():

    reports = Incident.query.order_by(
        Incident.created_at.desc()
    ).all()

    return jsonify({

        "success": True,

        "total_reports": len(reports),

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200


# =====================================================
# Get Pending Reports
#
# GET /api/admin/pending
# =====================================================

@admin_bp.route("/pending", methods=["GET"])
@official_required
def pending_reports():

    reports = Incident.query.filter_by(

        status="Pending"

    ).order_by(

        Incident.created_at.desc()

    ).all()

    return jsonify({

        "success": True,

        "total_reports": len(reports),

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200


# =====================================================
# Get Approved Reports
#
# GET /api/admin/approved
# =====================================================

@admin_bp.route("/approved", methods=["GET"])
@official_required
def approved_reports():

    reports = Incident.query.filter_by(

        status="Approved"

    ).order_by(

        Incident.created_at.desc()

    ).all()

    return jsonify({

        "success": True,

        "total_reports": len(reports),

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200


# =====================================================
# Get Rejected Reports
#
# GET /api/admin/rejected
# =====================================================

@admin_bp.route("/rejected", methods=["GET"])
@official_required
def rejected_reports():

    reports = Incident.query.filter_by(

        status="Rejected"

    ).order_by(

        Incident.created_at.desc()

    ).all()

    return jsonify({

        "success": True,

        "total_reports": len(reports),

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200


# =====================================================
# Get Single Incident
#
# GET /api/admin/incident/<id>
# =====================================================

@admin_bp.route("/incident/<int:incident_id>", methods=["GET"])
@official_required
def get_single_incident(incident_id):

    report = get_incident_or_404(

        incident_id

    )

    if report is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    return jsonify({

        "success": True,

        "incident": incident_to_dict(report)

    }), 200
# =====================================================
# Approve Incident
#
# PUT /api/admin/approve/<incident_id>
# =====================================================

@admin_bp.route("/approve/<int:incident_id>", methods=["PUT"])
@official_required
def approve_incident(incident_id):

    report = get_incident_or_404(incident_id)

    if report is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    data = request.get_json() or {}

    report.status = "Approved"

    report.admin_remark = data.get(

        "remark",

        "Verified by Disaster Management Authority."

    )

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Incident approved successfully.",

        "incident": incident_to_dict(report)

    }), 200


# =====================================================
# Reject Incident
#
# PUT /api/admin/reject/<incident_id>
# =====================================================

@admin_bp.route("/reject/<int:incident_id>", methods=["PUT"])
@official_required
def reject_incident(incident_id):

    report = get_incident_or_404(incident_id)

    if report is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    data = request.get_json() or {}

    report.status = "Rejected"

    report.admin_remark = data.get(

        "remark",

        "Report rejected after verification."

    )

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Incident rejected successfully.",

        "incident": incident_to_dict(report)

    }), 200


# =====================================================
# Update Admin Remark
#
# PUT /api/admin/remark/<incident_id>
# =====================================================

@admin_bp.route("/remark/<int:incident_id>", methods=["PUT"])
@official_required
def update_admin_remark(incident_id):

    report = get_incident_or_404(incident_id)

    if report is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    data = request.get_json()

    remark = data.get("remark")

    if not remark:

        return jsonify({

            "success": False,

            "message": "Remark is required."

        }), 400

    report.admin_remark = remark

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Admin remark updated successfully.",

        "incident": incident_to_dict(report)

    }), 200


# =====================================================
# Update Severity
#
# PUT /api/admin/severity/<incident_id>
# =====================================================

@admin_bp.route("/severity/<int:incident_id>", methods=["PUT"])
@official_required
def update_severity(incident_id):

    report = get_incident_or_404(incident_id)

    if report is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    data = request.get_json()

    severity = data.get("severity")

    valid_levels = [

        "Low",

        "Medium",

        "High",

        "Very High"

    ]

    if severity not in valid_levels:

        return jsonify({

            "success": False,

            "message": "Invalid severity."

        }), 400

    report.severity = severity

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Severity updated successfully.",

        "incident": incident_to_dict(report)

    }), 200
import os

# =====================================================
# Delete Incident
#
# DELETE /api/admin/delete/<incident_id>
# =====================================================

@admin_bp.route("/delete/<int:incident_id>", methods=["DELETE"])
@official_required
def delete_incident(incident_id):

    report = get_incident_or_404(incident_id)

    if report is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    # ---------------------------------------------
    # Delete Uploaded Image
    # ---------------------------------------------

    if report.image:

        image_path = os.path.join(

            Config.IMAGE_FOLDER,

            report.image

        )

        if os.path.exists(image_path):

            os.remove(image_path)

    # ---------------------------------------------
    # Delete Uploaded Video
    # ---------------------------------------------

    if report.video:

        video_path = os.path.join(

            Config.VIDEO_FOLDER,

            report.video

        )

        if os.path.exists(video_path):

            os.remove(video_path)

    db.session.delete(report)

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Incident deleted successfully."

    }), 200


# =====================================================
# Search Incidents
#
# GET /api/admin/search?q=
# =====================================================

@admin_bp.route("/search", methods=["GET"])
@official_required
def search_incidents():

    query = request.args.get("q", "")

    reports = Incident.query.filter(

        (Incident.title.ilike(f"%{query}%")) |

        (Incident.location.ilike(f"%{query}%")) |

        (Incident.district.ilike(f"%{query}%"))

    ).order_by(

        Incident.created_at.desc()

    ).all()

    return jsonify({

        "success": True,

        "total_reports": len(reports),

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200


# =====================================================
# Filter Incidents
#
# GET /api/admin/filter
#
# Example:
#
# ?severity=High
#
# ?status=Pending
#
# ?district=Tehri
# =====================================================

@admin_bp.route("/filter", methods=["GET"])
@official_required
def filter_reports():

    severity = request.args.get("severity")

    status = request.args.get("status")

    district = request.args.get("district")

    query = Incident.query

    if severity:

        query = query.filter_by(

            severity=severity

        )

    if status:

        query = query.filter_by(

            status=status

        )

    if district:

        query = query.filter_by(

            district=district

        )

    reports = query.order_by(

        Incident.created_at.desc()

    ).all()

    return jsonify({

        "success": True,

        "total_reports": len(reports),

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200


# =====================================================
# Incident Analytics
#
# GET /api/admin/analytics
# =====================================================

@admin_bp.route("/analytics", methods=["GET"])
@official_required
def analytics():

    low = Incident.query.filter_by(

        severity="Low"

    ).count()

    medium = Incident.query.filter_by(

        severity="Medium"

    ).count()

    high = Incident.query.filter_by(

        severity="High"

    ).count()

    very_high = Incident.query.filter_by(

        severity="Very High"

    ).count()

    return jsonify({

        "success": True,

        "analytics": {

            "Low": low,

            "Medium": medium,

            "High": high,

            "Very High": very_high

        }

    }), 200


# =====================================================
# Recent Incidents
#
# GET /api/admin/recent
# =====================================================

@admin_bp.route("/recent", methods=["GET"])
@official_required
def recent_incidents():

    reports = Incident.query.order_by(

        Incident.created_at.desc()

    ).limit(10).all()

    return jsonify({

        "success": True,

        "reports": [

            incident_to_dict(report)

            for report in reports

        ]

    }), 200