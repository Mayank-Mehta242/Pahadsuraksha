from flask import Blueprint, request, jsonify
from app.services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__, url_prefix="/api/weather")


@weather_bp.get("")
def weather():
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    if lat is None or lng is None:
        return jsonify({"error": "lat and lng query params are required."}), 400

    data = get_weather(lat, lng)
    return jsonify(data), 200
