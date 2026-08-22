import os
import uuid

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.incident import Incident
from app.utils.decorators import role_required

incidents_bp = Blueprint("incidents", __name__, url_prefix="/api/incidents")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@incidents_bp.get("")
def list_incidents():
    # Public map only shows approved reports; logged-in users could later
    # see their own pending ones too — left as a TODO for auth-scoped filtering.
    status = request.args.get("status")
    query = Incident.query
    if status:
        query = query.filter_by(status=status)
    incidents = query.order_by(Incident.created_at.desc()).all()
    return jsonify([i.to_dict() for i in incidents]), 200


@incidents_bp.post("")
def submit_incident():
    title = request.form.get("title")
    description = request.form.get("description")
    lat = request.form.get("lat", type=float)
    lng = request.form.get("lng", type=float)
    district = request.form.get("district")

    if not title or lat is None or lng is None:
        return jsonify({"error": "title, lat, and lng are required."}), 400

    image_path = None
    file = request.files.get("image")
    if file and file.filename:
        if not _allowed(file.filename):
            return jsonify({"error": "Unsupported image type."}), 400
        ext = file.filename.rsplit(".", 1)[1].lower()
        image_path = f"{uuid.uuid4()}.{ext}"
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(image_path)))

    reporter_id = None
    try:
        verify_jwt_in_request(optional=True)
        reporter_id = get_jwt_identity()
    except Exception:
        pass

    incident = Incident(
        title=title,
        description=description,
        district=district,
        lat=lat,
        lng=lng,
        image_path=image_path,
        reporter_id=reporter_id,
    )
    db.session.add(incident)
    db.session.commit()

    return jsonify(incident.to_dict()), 201


@incidents_bp.get("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@incidents_bp.patch("/<incident_id>/approve")
@role_required("district_officer")
def approve(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    body = request.get_json(silent=True) or {}
    incident.status = "approved"
    incident.review_comment = (body.get("comment") or "").strip()[:2000] or None
    db.session.commit()
    return jsonify(incident.to_dict()), 200


@incidents_bp.patch("/<incident_id>/reject")
@role_required("district_officer")
def reject(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    body = request.get_json(silent=True) or {}
    incident.status = "rejected"
    incident.review_comment = (body.get("comment") or "").strip()[:2000] or None
    db.session.commit()
    return jsonify(incident.to_dict()), 200


@incidents_bp.delete("/<incident_id>")
@role_required("district_officer")
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    if incident.status != "approved":
        return jsonify({"error": "Only approved reports can be deleted."}), 409

    if incident.image_path:
        image_file = os.path.join(current_app.config["UPLOAD_FOLDER"], secure_filename(incident.image_path))
        if os.path.isfile(image_file):
            os.remove(image_file)

    db.session.delete(incident)
    db.session.commit()
    return jsonify({"id": incident_id}), 200
