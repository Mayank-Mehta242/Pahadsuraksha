import requests

from flask import Blueprint
from flask import jsonify
from flask import request

from config import Config


# =====================================================
# Blueprint
# =====================================================

weather_bp = Blueprint(
    "weather",
    __name__
)


# =====================================================
# Weather API URLs
# =====================================================

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# =====================================================
# Road Safety Logic
# =====================================================

def get_road_status(rainfall, wind_speed):

    if rainfall >= 50:
        return {
            "level": "High Landslide Risk",
            "color": "red"
        }

    elif rainfall >= 20:
        return {
            "level": "Risky",
            "color": "orange"
        }

    elif rainfall >= 5:
        return {
            "level": "Moderate",
            "color": "yellow"
        }

    else:
        return {
            "level": "Safe",
            "color": "green"
        }


# =====================================================
# GET WEATHER
#
# Example:
#
# /api/weather?city=Tehri
#
# =====================================================

@weather_bp.route("/", methods=["GET"])
def get_weather():

    city = request.args.get("city")

    if not city:

        return jsonify({

            "message": "City is required."

        }), 400

    params = {

        "q": city,

        "appid": Config.OPENWEATHER_API_KEY,

        "units": "metric"

    }

    current_response = requests.get(

        CURRENT_WEATHER_URL,

        params=params

    )

    if current_response.status_code != 200:

        return jsonify({

            "message": "Unable to fetch weather."

        }), 500

    current = current_response.json()

    forecast_response = requests.get(

        FORECAST_URL,

        params=params

    )

    forecast = forecast_response.json()

    rainfall = 0

    if "rain" in current:

        rainfall = current["rain"].get("1h", 0)

    road_status = get_road_status(

        rainfall,

        current["wind"]["speed"]

    )

    hourly = []

    for item in forecast["list"][:8]:

        hourly.append({

            "time": item["dt_txt"],

            "temperature": item["main"]["temp"],

            "icon": item["weather"][0]["icon"]

        })

    weekly = []

    added = set()

    for item in forecast["list"]:

        day = item["dt_txt"].split(" ")[0]

        if day not in added:

            weekly.append({

                "day": day,

                "temperature": item["main"]["temp"],

                "icon": item["weather"][0]["icon"]

            })

            added.add(day)

    alerts = []

    if rainfall >= 50:

        alerts.append(

            "Heavy Rain Warning"

        )

    if current["wind"]["speed"] >= 15:

        alerts.append(

            "Strong Wind Warning"

        )

    if current["weather"][0]["main"] == "Thunderstorm":

        alerts.append(

            "Thunderstorm Alert"

        )

    return jsonify({

        "city": current["name"],

        "condition": current["weather"][0]["main"],

        "description": current["weather"][0]["description"],

        "icon": current["weather"][0]["icon"],

        "temperature": current["main"]["temp"],

        "feelsLike": current["main"]["feels_like"],

        "humidity": current["main"]["humidity"],

        "pressure": current["main"]["pressure"],

        "visibility": current["visibility"],

        "windSpeed": current["wind"]["speed"],

        "rainfall": rainfall,

        "updated": current["dt"],

        "roadStatus": road_status,

        "hourlyForecast": hourly,

        "weeklyForecast": weekly,

        "alerts": alerts

    })