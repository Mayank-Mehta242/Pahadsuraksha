from flask import Blueprint
from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

import requests

from config import Config

from models.user import User
from models.incident import Incident
from models.prediction import Prediction


# =====================================================
# Blueprint
# =====================================================

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# =====================================================
# OpenWeather API
# =====================================================

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


# =====================================================
# Default Dashboard City
#
# Change this later if required.
#
# Example:
#
# Tehri
#
# Dehradun
#
# Mussoorie
# =====================================================

DEFAULT_CITY = "Tehri"


# =====================================================
# Fetch Current Weather
# =====================================================

def get_live_weather(city=DEFAULT_CITY):

    params = {

        "q": city,

        "appid": Config.OPENWEATHER_API_KEY,

        "units": "metric"

    }

    response = requests.get(

        WEATHER_URL,

        params=params

    )

    if response.status_code != 200:

        return {

            "status": False,

            "message": "Unable to fetch weather."

        }

    data = response.json()

    rainfall = 0

    if "rain" in data:

        rainfall = data["rain"].get(

            "1h",

            0

        )

    return {

        "status": True,

        "city": data["name"],

        "condition": data["weather"][0]["main"],

        "description": data["weather"][0]["description"],

        "temperature": data["main"]["temp"],

        "feels_like": data["main"]["feels_like"],

        "humidity": data["main"]["humidity"],

        "pressure": data["main"]["pressure"],

        "visibility": data["visibility"],

        "wind_speed": data["wind"]["speed"],

        "rainfall": rainfall,

        "icon": data["weather"][0]["icon"]

    }


# =====================================================
# Road Safety Logic
# =====================================================

def road_status(weather):

    if weather["status"] is False:

        return "Unknown"

    rain = weather["rainfall"]

    if rain >= 50:

        return "High Landslide Risk"

    elif rain >= 20:

        return "Risky"

    elif rain >= 5:

        return "Moderate"

    else:

        return "Safe"


# =====================================================
# Get Logged In User
# =====================================================

def current_user():

    user_id = get_jwt_identity()

    return User.query.get(user_id)
# =====================================================
# Dashboard Statistics
# =====================================================

def dashboard_statistics():

    total_users = User.query.count()

    total_incidents = Incident.query.count()

    total_predictions = Prediction.query.count()

    pending_reports = Incident.query.filter_by(
        status="Pending"
    ).count()

    approved_reports = Incident.query.filter_by(
        status="Approved"
    ).count()

    rejected_reports = Incident.query.filter_by(
        status="Rejected"
    ).count()

    return {

        "totalUsers": total_users,

        "totalIncidents": total_incidents,

        "totalPredictions": total_predictions,

        "pendingReports": pending_reports,

        "approvedReports": approved_reports,

        "rejectedReports": rejected_reports

    }


# =====================================================
# Severity Analytics
# =====================================================

def severity_statistics():

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

    return {

        "Low": low,

        "Medium": medium,

        "High": high,

        "Very High": very_high

    }


# =====================================================
# Prediction Analytics
# =====================================================

def prediction_statistics():

    low = Prediction.query.filter_by(
        risk_level="Low"
    ).count()

    medium = Prediction.query.filter_by(
        risk_level="Medium"
    ).count()

    high = Prediction.query.filter_by(
        risk_level="High"
    ).count()

    very_high = Prediction.query.filter_by(
        risk_level="Very High"
    ).count()

    return {

        "Low": low,

        "Medium": medium,

        "High": high,

        "Very High": very_high

    }


# =====================================================
# Latest Dashboard Counts
# =====================================================

def latest_counts():

    return {

        "latestIncident":

            Incident.query.order_by(

                Incident.created_at.desc()

            ).first(),

        "latestPrediction":

            Prediction.query.order_by(

                Prediction.created_at.desc()

            ).first()

    }


# =====================================================
# Dashboard Summary
# =====================================================

def dashboard_summary():

    weather = get_live_weather()

    return {

        "statistics": dashboard_statistics(),

        "severity": severity_statistics(),

        "predictionStats": prediction_statistics(),

        "roadStatus": road_status(weather)

    }
# =====================================================
# Recent Incidents
#
# Returns latest approved incidents
# =====================================================

def recent_incidents(limit=5):

    reports = Incident.query.filter_by(

        status="Approved"

    ).order_by(

        Incident.created_at.desc()

    ).limit(limit).all()

    data = []

    for report in reports:

        data.append({

            "id": report.id,

            "title": report.title,

            "location": report.location,

            "district": report.district,

            "severity": report.severity,

            "status": report.status,

            "created_at": report.created_at

        })

    return data


# =====================================================
# Latest Predictions
#
# Returns latest AI predictions
# =====================================================

def recent_predictions(limit=5):

    predictions = Prediction.query.order_by(

        Prediction.created_at.desc()

    ).limit(limit).all()

    data = []

    for prediction in predictions:

        data.append({

            "id": prediction.id,

            "source": prediction.source,

            "destination": prediction.destination,

            "risk": prediction.risk_level,

            "confidence": prediction.confidence,

            "recommendation": prediction.recommendation,

            "created_at": prediction.created_at

        })

    return data


# =====================================================
# Logged In User Prediction History
# =====================================================

def user_prediction_history(user_id, limit=5):

    predictions = Prediction.query.filter_by(

        user_id=user_id

    ).order_by(

        Prediction.created_at.desc()

    ).limit(limit).all()

    history = []

    for prediction in predictions:

        history.append({

            "id": prediction.id,

            "source": prediction.source,

            "destination": prediction.destination,

            "risk": prediction.risk_level,

            "confidence": prediction.confidence,

            "recommendation": prediction.recommendation,

            "created_at": prediction.created_at

        })

    return history


# =====================================================
# Logged In User Reports
# =====================================================

def user_reports(user_id, limit=5):

    reports = Incident.query.filter_by(

        user_id=user_id

    ).order_by(

        Incident.created_at.desc()

    ).limit(limit).all()

    data = []

    for report in reports:

        data.append({

            "id": report.id,

            "title": report.title,

            "location": report.location,

            "severity": report.severity,

            "status": report.status,

            "created_at": report.created_at

        })

    return data


# =====================================================
# Dashboard Weather Section
# =====================================================

def weather_section():

    weather = get_live_weather()

    if weather["status"] is False:

        return weather

    weather["roadSafety"] = road_status(weather)

    return weather
# =====================================================
# Dashboard API
#
# GET /api/dashboard
#
# Returns:
#
# • Dashboard Statistics
# • Live Weather
# • Road Safety
# • Recent Incidents
# • Recent Predictions
# • User History
#
# Dashboard automatically changes according
# to Citizen / Official login.
# =====================================================

@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def dashboard():

    user = current_user()

    if user is None:

        return jsonify({

            "success": False,

            "message": "User not found."

        }), 404

    weather = weather_section()

    summary = dashboard_summary()

    latest = latest_counts()

    response = {

        "success": True,

        "user": {

            "id": user.id,

            "name": user.name,

            "email": user.email,

            "role": user.role

        },

        # ============================================
        # Dashboard Cards
        # ============================================

        "statistics": summary["statistics"],

        # ============================================
        # Pie Chart
        # ============================================

        "severityAnalytics": summary["severity"],

        # ============================================
        # AI Prediction Chart
        # ============================================

        "predictionAnalytics":

            summary["predictionStats"],

        # ============================================
        # Live Weather
        # ============================================

        "weather": weather,

        # ============================================
        # Road Safety
        # ============================================

        "roadSafety":

            summary["roadStatus"],

        # ============================================
        # Latest Incident
        # ============================================

        "latestIncident":

            None

            if latest["latestIncident"] is None

            else {

                "id":

                    latest["latestIncident"].id,

                "title":

                    latest["latestIncident"].title,

                "location":

                    latest["latestIncident"].location,

                "severity":

                    latest["latestIncident"].severity,

                "status":

                    latest["latestIncident"].status

            },

        # ============================================
        # Latest Prediction
        # ============================================

        "latestPrediction":

            None

            if latest["latestPrediction"] is None

            else {

                "id":

                    latest["latestPrediction"].id,

                "source":

                    latest["latestPrediction"].source,

                "destination":

                    latest["latestPrediction"].destination,

                "risk":

                    latest["latestPrediction"].risk_level,

                "recommendation":

                    latest["latestPrediction"].recommendation

            },

        # ============================================
        # Recent Approved Incidents
        # ============================================

        "recentIncidents":

            recent_incidents(),

        # ============================================
        # Latest AI Predictions
        # ============================================

        "recentPredictions":

            recent_predictions(),

        # ============================================
        # Logged In User History
        # ============================================

        "myPredictions":

            user_prediction_history(user.id),

        "myReports":

            user_reports(user.id)

    }

    # ==================================================
    # Official Dashboard
    #
    # Only visible to Officials/Admins
    # ==================================================

    if user.role == "Official":

        response["admin"] = {

            "dashboardStatistics":

                dashboard_statistics(),

            "severityAnalytics":

                severity_statistics(),

            "predictionAnalytics":

                prediction_statistics(),

            "pendingReports":

                Incident.query.filter_by(

                    status="Pending"

                ).count(),

            "approvedReports":

                Incident.query.filter_by(

                    status="Approved"

                ).count(),

            "rejectedReports":

                Incident.query.filter_by(

                    status="Rejected"

                ).count()

        }

    return jsonify(response), 200