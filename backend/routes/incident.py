import os
import uuid

from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from werkzeug.utils import secure_filename

from config import Config

from models import db
from models.incident import Incident


# =====================================================
# Blueprint
# =====================================================

incident_bp = Blueprint(
    "incident",
    __name__
)


# =====================================================
# Allowed File Extensions
# =====================================================

IMAGE_EXTENSIONS = {

    "png",

    "jpg",

    "jpeg"

}

VIDEO_EXTENSIONS = {

    "mp4",

    "mov",

    "avi",

    "mkv"

}


# =====================================================
# Check File Extension
# =====================================================

def allowed_image(filename):

    if "." not in filename:

        return False

    extension = filename.rsplit(

        ".",

        1

    )[1].lower()

    return extension in IMAGE_EXTENSIONS


def allowed_video(filename):

    if "." not in filename:

        return False

    extension = filename.rsplit(

        ".",

        1

    )[1].lower()

    return extension in VIDEO_EXTENSIONS


# =====================================================
# Save Uploaded Image
# =====================================================

def save_image(file):

    if file is None:

        return None

    if file.filename == "":

        return None

    if not allowed_image(file.filename):

        return None

    filename = (

        str(uuid.uuid4())

        + "_"

        + secure_filename(file.filename)

    )

    filepath = os.path.join(

        Config.IMAGE_FOLDER,

        filename

    )

    os.makedirs(

        Config.IMAGE_FOLDER,

        exist_ok=True

    )

    file.save(filepath)

    return filename


# =====================================================
# Save Uploaded Video
# =====================================================

def save_video(file):

    if file is None:

        return None

    if file.filename == "":

        return None

    if not allowed_video(file.filename):

        return None

    filename = (

        str(uuid.uuid4())

        + "_"

        + secure_filename(file.filename)

    )

    filepath = os.path.join(

        Config.VIDEO_FOLDER,

        filename

    )

    os.makedirs(

        Config.VIDEO_FOLDER,

        exist_ok=True

    )

    file.save(filepath)

    return filename


# =====================================================
# Incident Status
# =====================================================

PENDING = "Pending"

APPROVED = "Approved"

REJECTED = "Rejected"
# =====================================================
# Submit Incident
#
# POST /api/incident/report
#
# Form Data
#
# title
# description
# location
# district
# severity
# image
# video
#
# =====================================================

@incident_bp.route("/report", methods=["POST"])
@jwt_required()
def report_incident():

    # -------------------------------------------------
    # Logged In User
    # -------------------------------------------------

    user_id = get_jwt_identity()

    # -------------------------------------------------
    # Get Form Data
    # -------------------------------------------------

    title = request.form.get("title")

    description = request.form.get("description")

    location = request.form.get("location")

    district = request.form.get("district")

    severity = request.form.get("severity")

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    if not title:

        return jsonify({

            "success": False,

            "message": "Title is required."

        }), 400

    if not description:

        return jsonify({

            "success": False,

            "message": "Description is required."

        }), 400

    if not location:

        return jsonify({

            "success": False,

            "message": "Location is required."

        }), 400

    if not district:

        return jsonify({

            "success": False,

            "message": "District is required."

        }), 400

    if severity not in [

        "Low",

        "Medium",

        "High",

        "Very High"

    ]:

        return jsonify({

            "success": False,

            "message": "Invalid severity."

        }), 400

    # -------------------------------------------------
    # Upload Image
    # -------------------------------------------------

    image_file = request.files.get("image")

    image_name = save_image(

        image_file

    )

    # -------------------------------------------------
    # Upload Video
    # -------------------------------------------------

    video_file = request.files.get("video")

    video_name = save_video(

        video_file

    )

    # -------------------------------------------------
    # Create Incident
    # -------------------------------------------------

    incident = Incident(

        title=title,

        description=description,

        location=location,

        district=district,

        severity=severity,

        image=image_name,

        video=video_name,

        status=PENDING,

        user_id=user_id

    )

    # -------------------------------------------------
    # Save to Database
    # -------------------------------------------------

    db.session.add(

        incident

    )

    db.session.commit()

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

    return jsonify({

        "success": True,

        "message": "Incident submitted successfully.",

        "incident": {

            "id": incident.id,

            "title": incident.title,

            "location": incident.location,

            "district": incident.district,

            "severity": incident.severity,

            "status": incident.status,

            "image": incident.image,

            "video": incident.video,

            "created_at": incident.created_at

        }

    }), 201
# =====================================================
# Get Logged In User's Reports
#
# GET /api/incident/my-reports
# =====================================================

@incident_bp.route("/my-reports", methods=["GET"])
@jwt_required()
def my_reports():

    user_id = get_jwt_identity()

    reports = Incident.query.filter_by(
        user_id=user_id
    ).order_by(
        Incident.created_at.desc()
    ).all()

    report_list = []

    for report in reports:

        report_list.append({

            "id": report.id,

            "title": report.title,

            "description": report.description,

            "location": report.location,

            "district": report.district,

            "severity": report.severity,

            "status": report.status,

            "image": report.image,

            "video": report.video,

            "created_at": report.created_at

        })

    return jsonify({

        "success": True,

        "total_reports": len(report_list),

        "reports": report_list

    }), 200


# =====================================================
# Get All Approved Reports
#
# Used By:
#
# Dashboard
#
# Leaflet Map
#
# Recent Incidents
#
# GET /api/incident/approved
# =====================================================

@incident_bp.route("/approved", methods=["GET"])
def approved_reports():

    reports = Incident.query.filter_by(

        status=APPROVED

    ).order_by(

        Incident.created_at.desc()

    ).all()

    approved = []

    for report in reports:

        approved.append({

            "id": report.id,

            "title": report.title,

            "description": report.description,

            "location": report.location,

            "district": report.district,

            "severity": report.severity,

            "image": report.image,

            "video": report.video,

            "created_at": report.created_at

        })

    return jsonify({

        "success": True,

        "total_reports": len(approved),

        "reports": approved

    }), 200


# =====================================================
# Get Single Incident
#
# GET /api/incident/<id>
# =====================================================

@incident_bp.route("/<int:incident_id>", methods=["GET"])
def get_incident(incident_id):

    incident = Incident.query.get(incident_id)

    if incident is None:

        return jsonify({

            "success": False,

            "message": "Incident not found."

        }), 404

    return jsonify({

        "success": True,

        "incident": {

            "id": incident.id,

            "title": incident.title,

            "description": incident.description,

            "location": incident.location,

            "district": incident.district,

            "severity": incident.severity,

            "status": incident.status,

            "image": incident.image,

            "video": incident.video,

            "admin_remark": incident.admin_remark,

            "user_id": incident.user_id,

            "created_at": incident.created_at,

            "updated_at": incident.updated_at

        }

    }), 200
