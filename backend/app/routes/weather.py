from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__, url_prefix="/api/weather")

TEHRI_GARHWAL = (30.3752, 78.48)


@weather_bp.get("")
def weather():
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    if lat is None and lng is None:
        lat, lng = TEHRI_GARHWAL
    elif lat is None or lng is None:
        return jsonify({"error": "lat and lng query params must be provided together."}), 400

    data = get_weather(lat, lng)
    return jsonify(data), 200
