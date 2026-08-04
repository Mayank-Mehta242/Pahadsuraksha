import os
import joblib
import requests

from flask import Blueprint
from flask import request
from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from config import Config

from models import db
from models.prediction import Prediction

# =====================================================
# Blueprint
# =====================================================

prediction_bp = Blueprint(
    "prediction",
    __name__
)

# =====================================================
# API URLs
# =====================================================

GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"

DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# =====================================================
# Load AI Model
# =====================================================

MODEL = None

try:

    MODEL = joblib.load(Config.MODEL_PATH)

    print("AI Model Loaded Successfully.")

except Exception as e:

    print("Unable to load AI Model.")

    print(e)

# =====================================================
# Recommendation Logic
# =====================================================

def get_recommendation(risk):

    risk = risk.lower()

    if risk == "low":

        return "Safe Journey"

    elif risk == "medium":

        return "Travel with Caution"

    elif risk == "high":

        return "Avoid unnecessary travel"

    elif risk == "very high":

        return (
            "High Landslide Risk. "
            "Avoid travelling completely."
        )

    return "Recommendation unavailable"

# =====================================================
# Geocoding Function
#
# Converts
#
# Dehradun
#
# ->
#
# Latitude
#
# Longitude
# =====================================================

def get_coordinates(location):

    location_key = str(location).strip().lower()

    fallback_coordinates = {
        "dehradun": {"latitude": 30.3165, "longitude": 78.0322},
        "mussoorie": {"latitude": 30.4599, "longitude": 78.0669},
        "tehri": {"latitude": 30.3772, "longitude": 78.4802},
        "uttarkashi": {"latitude": 30.7282, "longitude": 78.4470},
        "haridwar": {"latitude": 29.9457, "longitude": 78.1642},
        "rishikesh": {"latitude": 30.0869, "longitude": 78.2676},
        "nainital": {"latitude": 29.3919, "longitude": 79.4542},
        "almora": {"latitude": 29.5972, "longitude": 79.6592},
        "pithoragarh": {"latitude": 29.5820, "longitude": 80.2185},
        "bageshwar": {"latitude": 29.8523, "longitude": 79.7662},
        "champawat": {"latitude": 29.3324, "longitude": 80.1036},
        "rudraprayag": {"latitude": 30.2830, "longitude": 78.9830}
    }

    if location_key in fallback_coordinates:
        return fallback_coordinates[location_key]

    headers = {

        "Authorization":
        Config.OPENROUTESERVICE_API_KEY

    }

    params = {

        "text": location,

        "size": 1

    }

    response = requests.get(

        GEOCODE_URL,

        headers=headers,

        params=params

    )

    if response.status_code != 200:

        return None

    data = response.json()

    if len(data["features"]) == 0:

        return None

    coordinates = data["features"][0]["geometry"]["coordinates"]

    return {

        "longitude": coordinates[0],

        "latitude": coordinates[1]

    }

# =====================================================
# Weather Function
#
# Returns
#
# Temperature
#
# Humidity
#
# Rainfall
#
# Wind Speed
# =====================================================

def get_weather(lat, lon):

    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
        return {
            "condition": "Clouds",
            "temperature": 18,
            "humidity": 70,
            "rainfall": 12,
            "wind_speed": 8,
            "pressure": 1012,
            "visibility": 10000
        }

    params = {

        "lat": lat,

        "lon": lon,

        "appid": Config.OPENWEATHER_API_KEY,

        "units": "metric"

    }

    response = requests.get(

        WEATHER_URL,

        params=params

    )

    if response.status_code != 200:

        return None

    weather = response.json()

    rainfall = 0

    if "rain" in weather:

        rainfall = weather["rain"].get("1h", 0)

    return {

        "condition":
            weather["weather"][0]["main"],

        "temperature":
            weather["main"]["temp"],

        "humidity":
            weather["main"]["humidity"],

        "rainfall":
            rainfall,

        "wind_speed":
            weather["wind"]["speed"],

        "pressure":
            weather["main"]["pressure"],

        "visibility":
            weather["visibility"]
    }
# =====================================================
# Route Function
#
# Returns:
# Distance
# Duration
# Route Coordinates
# =====================================================

def get_route(source, destination):

    headers = {
        "Authorization": Config.OPENROUTESERVICE_API_KEY,
        "Content-Type": "application/json"
    }

    body = {

        "coordinates": [

            [
                source["longitude"],
                source["latitude"]
            ],

            [
                destination["longitude"],
                destination["latitude"]
            ]

        ]

    }

    response = requests.post(

        DIRECTIONS_URL,

        headers=headers,

        json=body

    )

    if response.status_code != 200:

        from math import radians, sin, cos, sqrt, atan2

        lat1 = radians(source["latitude"])
        lon1 = radians(source["longitude"])
        lat2 = radians(destination["latitude"])
        lon2 = radians(destination["longitude"])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = 6371 * c

        return {
            "distance": round(distance_km, 2),
            "duration": round(distance_km / 40 * 60, 2),
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [source["longitude"], source["latitude"]],
                    [destination["longitude"], destination["latitude"]]
                ]
            }
        }

    data = response.json()

    summary = data["routes"][0]["summary"]

    geometry = data["routes"][0]["geometry"]

    return {

        "distance": round(
            summary["distance"] / 1000,
            2
        ),

        "duration": round(
            summary["duration"] / 60,
            2
        ),

        "geometry": geometry

    }


# =====================================================
# AI Prediction Function
#
# Input:
#
# Weather Data
#
# Output:
#
# Risk Level
#
# Confidence
# =====================================================

def predict_risk(weather):

    # --------------------------------------------
    # If AI model is not available
    # --------------------------------------------

    if MODEL is None:

        rainfall = weather["rainfall"]

        if rainfall < 5:

            risk = "Low"

        elif rainfall < 20:

            risk = "Medium"

        elif rainfall < 50:

            risk = "High"

        else:

            risk = "Very High"

        return {

            "risk": risk,

            "confidence": 70

        }

    # --------------------------------------------
    # Prepare Features
    # Order should match train_model.py
    # --------------------------------------------

    features = [[

        weather["rainfall"],

        weather["humidity"],

        weather["temperature"],

        weather["wind_speed"],

        weather["pressure"],

        weather["visibility"]

    ]]

    # --------------------------------------------
    # AI Prediction
    # --------------------------------------------

    prediction = MODEL.predict(features)[0]

    confidence = max(

        MODEL.predict_proba(features)[0]

    ) * 100

    # --------------------------------------------
    # Convert Number → Label
    # --------------------------------------------

    risk_map = {

        0: "Low",

        1: "Medium",

        2: "High",

        3: "Very High"

    }

    return {

        "risk": risk_map.get(

            prediction,

            "Unknown"

        ),

        "confidence": round(

            confidence,

            2

        )

    }


# =====================================================
# Format Travel Time
#
# Example:
#
# 142 minutes
#
# ->
#
# 2 hr 22 min
# =====================================================

def format_duration(minutes):

    hours = int(minutes // 60)

    mins = int(minutes % 60)

    if hours == 0:

        return f"{mins} min"

    return f"{hours} hr {mins} min"
# =====================================================
# Predict Route
#
# POST /api/prediction
# =====================================================

@prediction_bp.route("/", methods=["POST"])
@jwt_required()
def predict():

    # -------------------------------------------------
    # Logged In User
    # -------------------------------------------------

    user_id = get_jwt_identity()

    # -------------------------------------------------
    # Request Body
    # -------------------------------------------------

    data = request.get_json()

    source_name = data.get("source")
    destination_name = data.get("destination")

    if not source_name or not destination_name:

        return jsonify({

            "message": "Source and Destination are required."

        }), 400

    # -------------------------------------------------
    # Get Coordinates
    # -------------------------------------------------

    source = get_coordinates(source_name)

    if source is None:

        return jsonify({

            "message": "Invalid Source."

        }), 400

    destination = get_coordinates(destination_name)

    if destination is None:

        return jsonify({

            "message": "Invalid Destination."

        }), 400

    # -------------------------------------------------
    # Get Route
    # -------------------------------------------------

    route = get_route(

        source,

        destination

    )

    if route is None:

        return jsonify({

            "message": "Unable to calculate route."

        }), 500

    # -------------------------------------------------
    # Get Weather
    #
    # Current implementation:
    # Weather is fetched for the SOURCE location.
    #
    # Future Improvement:
    # Fetch weather from multiple points along the route
    # and average the conditions.
    # -------------------------------------------------

    weather = get_weather(

        source["latitude"],

        source["longitude"]

    )

    if weather is None:

        return jsonify({

            "message": "Unable to fetch weather."

        }), 500

    # -------------------------------------------------
    # AI Prediction
    # -------------------------------------------------

    ai_result = predict_risk(

        weather

    )

    # -------------------------------------------------
    # Travel Recommendation
    # -------------------------------------------------

    recommendation = get_recommendation(

        ai_result["risk"]

    )
        # -------------------------------------------------
    # Save Prediction
    # -------------------------------------------------

    prediction = Prediction(

        user_id=user_id,

        source=source_name,

        destination=destination_name,

        weather_condition=weather["condition"],

        rainfall=weather["rainfall"],

        humidity=weather["humidity"],

        temperature=weather["temperature"],

        wind_speed=weather["wind_speed"],

        pressure=weather["pressure"],

        visibility=weather["visibility"],

        uv_index=0,      # Replace later with UV API

        risk_level=ai_result["risk"],

        confidence=ai_result["confidence"],

        recommendation=recommendation,

        distance=route["distance"],

        estimated_time=format_duration(

            route["duration"]

        )

    )

    db.session.add(

        prediction

    )

    db.session.commit()
        # -------------------------------------------------
    # Return Response to React Frontend
    # -------------------------------------------------

    return jsonify({

        "success": True,

        "message": "Prediction generated successfully.",

        "prediction_id": prediction.id,

        # =============================================
        # Route Information
        # =============================================

        "route": {

            "source": source_name,

            "destination": destination_name,

            "distance_km": route["distance"],

            "estimated_time": format_duration(
                route["duration"]
            ),

            # -----------------------------------------
            # Use this in Leaflet React Map
            # -----------------------------------------

            "geometry": route["geometry"]

        },

        # =============================================
        # Weather Information
        # =============================================

        "weather": {

            "condition": weather["condition"],

            "temperature": weather["temperature"],

            "humidity": weather["humidity"],

            "rainfall": weather["rainfall"],

            "wind_speed": weather["wind_speed"],

            "pressure": weather["pressure"],

            "visibility": weather["visibility"]

        },

        # =============================================
        # AI Prediction
        # =============================================

        "prediction": {

            "risk": ai_result["risk"],

            "confidence": ai_result["confidence"],

            "recommendation": recommendation

        }

    }), 200


# =====================================================
# Prediction History
#
# GET /api/prediction/history
# =====================================================

@prediction_bp.route("/history", methods=["GET"])
@jwt_required()
def prediction_history():

    user_id = get_jwt_identity()

    predictions = Prediction.query.filter_by(
        user_id=user_id
    ).order_by(
        Prediction.created_at.desc()
    ).all()

    return jsonify({

        "success": True,

        "total_predictions": len(predictions),

        "history": [

            prediction.to_dict()

            for prediction in predictions

        ]

    }), 200


# =====================================================
# Get One Prediction
#
# GET /api/prediction/<id>
# =====================================================

@prediction_bp.route("/<int:prediction_id>", methods=["GET"])
@jwt_required()
def get_prediction(prediction_id):

    prediction = Prediction.query.get(prediction_id)

    if prediction is None:

        return jsonify({

            "success": False,

            "message": "Prediction not found."

        }), 404

    return jsonify({

        "success": True,

        "prediction": prediction.to_dict()

    }), 200