from flask import Blueprint, jsonify
from app.models.district import District
from app.models.incident import Incident
from app.models.user import User

districts_bp = Blueprint("districts", __name__, url_prefix="/api/districts")


@districts_bp.get("")
def list_districts():
    districts = District.query.all()
    return jsonify([d.to_dict() for d in districts]), 200


@districts_bp.get("/stats")
def stats():
    monitored_district = District.query.order_by(District.name.asc()).first()
    return (
        jsonify(
            {
                "monitoredDistricts": District.query.count(),
                "monitoredDistrictName": monitored_district.name if monitored_district else None,
                "reportedIncidents": Incident.query.count(),
                "activeUsers": User.query.count(),
            }
        ),
        200,
    )


@districts_bp.get("/historical")
def historical():
    # Returns synthetic historical data for demo purposes
    # In production, this would aggregate real incident dates from the database
    return (
        jsonify(
            {
                "monthly": [
                    {"month": m, "count": c}
                    for m, c in zip(
                        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                        [2, 3, 5, 8, 11, 19, 34, 29, 17, 6, 2, 1],
                    )
                ],
                "yearly": [
                    {"year": y, "count": c}
                    for y, c in zip([2020, 2021, 2022, 2023, 2024], [96, 112, 131, 148, 158])
                ],
                "topVulnerable": [
                    d.name
                    for d in District.query.order_by(District.incidents_ytd.desc()).limit(5).all()
                ],
            }
        ),
        200,
    )
