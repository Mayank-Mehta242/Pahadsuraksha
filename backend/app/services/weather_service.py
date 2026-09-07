"""Fetch current and forecast weather from RapidAPI with a DB-backed cache."""
import json
from datetime import datetime, timedelta, timezone

import requests
from flask import current_app

from app.extensions import db
from app.models.weather_cache import WeatherCache

RAPIDAPI_URL = "https://open-weather13.p.rapidapi.com"


def _to_celsius(value):
    return value - 273.15


def _round_key(value):
    # ~1km grid so nearby clicks share a cache entry
    return round(value, 2)


def get_weather(lat: float, lng: float):
    lat_key, lng_key = _round_key(lat), _round_key(lng)
    cache_minutes = current_app.config["WEATHER_CACHE_MINUTES"]

    cached = (
        WeatherCache.query.filter_by(lat_key=lat_key, lng_key=lng_key)
        .order_by(WeatherCache.fetched_at.desc())
        .first()
    )
    legacy_cache = (
        "OPENWEATHER_API_KEY" in (cached.location_name or "")
        or "OPENWEATHER_API_KEY" in (cached.condition or "")
        or "RapidAPI key not configured" in (cached.location_name or "")
    ) if cached else False
    if cached and not legacy_cache:
        fetched_at = cached.fetched_at
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=timezone.utc)
        if fetched_at > datetime.now(timezone.utc) - timedelta(minutes=cache_minutes):
            return _cache_to_dict(cached)

    data = _fetch_from_rapidapi(lat, lng) if current_app.config["RAPIDAPI_KEY"] else _synthetic_weather()

    entry = WeatherCache(
        lat_key=lat_key,
        lng_key=lng_key,
        location_name=data["location"],
        temperature_c=data["temperatureC"],
        humidity_pct=data["humidityPct"],
        rainfall_mm=data["rainfallMm"],
        wind_kmh=data["windKmh"],
        elevation_m=data.get("elevationM"),
        condition=data["condition"],
        forecast_json=json.dumps(data["forecast"]),
    )
    db.session.add(entry)
    db.session.commit()

    return data


def _fetch_from_rapidapi(lat, lng):
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": current_app.config["RAPIDAPI_HOST"],
        "x-rapidapi-key": current_app.config["RAPIDAPI_KEY"],
        "x-rapidapi-ua": current_app.config["RAPIDAPI_UA"],
    }
    current_response = requests.get(
        f"{RAPIDAPI_URL}/latlon",
        params={"latitude": lat, "longitude": lng, "lang": "EN"},
        headers=headers,
        timeout=8,
    )
    current_response.raise_for_status()
    current = current_response.json()

    forecast = _fetch_forecast(lat, lng, headers, current)
    rainfall = current.get("rain", {}).get("1h", current.get("rain", {}).get("3h", 0))
    location = current.get("name") or f"{lat:.2f}, {lng:.2f}"
    if current.get("sys", {}).get("country"):
        location = f"{location}, {current['sys']['country']}"

    return {
        "location": location,
        "temperatureC": round(_to_celsius(current["main"]["temp"]), 1),
        "humidityPct": current["main"]["humidity"],
        "rainfallMm": round(rainfall, 1),
        "windKmh": round(current.get("wind", {}).get("speed", 0) * 3.6, 1),
        "elevationM": None,  # Elevation API integration planned for future
        "condition": current["weather"][0]["description"].title() if current.get("weather") else "Unknown",
        "forecast": forecast,
    }


def _fetch_forecast(lat, lng, headers, current):
    try:
        response = requests.get(
            f"{RAPIDAPI_URL}/fivedaysforcast",
            params={"latitude": lat, "longitude": lng, "lang": "EN"},
            headers=headers,
            timeout=8,
        )
        response.raise_for_status()
        entries = response.json().get("list", [])
        forecast = []
        for entry in entries[::8][:5]:
            forecast.append(
                {
                    "day": datetime.fromtimestamp(entry["dt"], tz=timezone.utc).strftime("%a"),
                    "tempC": round(_to_celsius(entry["main"]["temp"]), 1),
                    "rainMm": round(entry.get("rain", {}).get("3h", 0), 1),
                    "humidityPct": entry["main"]["humidity"],
                }
            )
        if forecast:
            return forecast
    except (KeyError, TypeError, ValueError, requests.RequestException):
        pass

    now = datetime.now(timezone.utc)
    return [
        {
            "day": now.strftime("%a"),
            "tempC": round(_to_celsius(current["main"]["temp"]), 1),
            "rainMm": round(current.get("rain", {}).get("1h", 0), 1),
            "humidityPct": current["main"]["humidity"],
        }
    ]


def _synthetic_weather():
    """Used only when no RAPIDAPI_KEY is configured, so local dev
    still returns a well-shaped response instead of erroring out."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {
        "location": "Tehri Garhwal (RapidAPI key not configured)",
        "temperatureC": 16,
        "humidityPct": 70,
        "rainfallMm": 10,
        "windKmh": 12,
        "elevationM": None,
        "condition": "Data unavailable - set RAPIDAPI_KEY",
        "forecast": [{"day": d, "tempC": 16, "rainMm": 10, "humidityPct": 70} for d in days],
    }


def _cache_to_dict(entry: WeatherCache):
    forecast = json.loads(entry.forecast_json) if entry.forecast_json else []
    if entry.temperature_c > 100:
        temperature_c = round(_to_celsius(entry.temperature_c), 1)
        forecast = [
            {**item, "tempC": round(_to_celsius(item["tempC"]), 1) if item.get("tempC", 0) > 100 else item["tempC"]}
            for item in forecast
        ]
    else:
        temperature_c = entry.temperature_c
    return {
        "location": entry.location_name,
        "temperatureC": temperature_c,
        "humidityPct": entry.humidity_pct,
        "rainfallMm": entry.rainfall_mm,
        "windKmh": entry.wind_kmh,
        "elevationM": entry.elevation_m,
        "condition": entry.condition,
        "forecast": forecast,
    }
