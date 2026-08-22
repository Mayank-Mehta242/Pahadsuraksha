"""
Fetches current + forecast weather from OpenWeather, with a simple
DB-backed cache so we don't hammer the API for the same location.

Requires OPENWEATHER_API_KEY in .env. Without a key, falls back to a
clearly-labelled synthetic reading so the endpoint still works in dev.
"""
import json
from datetime import datetime, timedelta, timezone

import requests
from flask import current_app

from app.extensions import db
from app.models.weather_cache import WeatherCache

OPENWEATHER_URL = "https://api.openweathermap.org/data/3.0/onecall"


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
    if cached:
        fetched_at = cached.fetched_at
        if fetched_at.tzinfo is None:
            fetched_at = fetched_at.replace(tzinfo=timezone.utc)
        if fetched_at > datetime.now(timezone.utc) - timedelta(minutes=cache_minutes):
            return _cache_to_dict(cached)

    data = _fetch_from_openweather(lat, lng) if current_app.config["OPENWEATHER_API_KEY"] else _synthetic_weather()

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


def _fetch_from_openweather(lat, lng):
    params = {
        "lat": lat,
        "lon": lng,
        "appid": current_app.config["OPENWEATHER_API_KEY"],
        "units": "metric",
        "exclude": "minutely,alerts",
    }
    resp = requests.get(OPENWEATHER_URL, params=params, timeout=8)
    resp.raise_for_status()
    payload = resp.json()

    current = payload["current"]
    daily = payload.get("daily", [])[:7]

    forecast = []
    for day in daily:
        dt = datetime.fromtimestamp(day["dt"], tz=timezone.utc)
        forecast.append(
            {
                "day": dt.strftime("%a"),
                "tempC": round(day["temp"]["day"], 1),
                "rainMm": round(day.get("rain", 0), 1),
                "humidityPct": day["humidity"],
            }
        )

    return {
        "location": f"{lat:.2f}, {lng:.2f}",
        "temperatureC": round(current["temp"], 1),
        "humidityPct": current["humidity"],
        "rainfallMm": round(current.get("rain", {}).get("1h", 0), 1),
        "windKmh": round(current["wind_speed"] * 3.6, 1),
        "elevationM": None,  # Elevation API integration planned for future
        "condition": current["weather"][0]["description"].title() if current.get("weather") else "Unknown",
        "forecast": forecast,
    }


def _synthetic_weather():
    """Used only when no OPENWEATHER_API_KEY is configured, so local dev
    still returns a well-shaped response instead of erroring out."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {
        "location": "Unknown (no OPENWEATHER_API_KEY set)",
        "temperatureC": 16,
        "humidityPct": 70,
        "rainfallMm": 10,
        "windKmh": 12,
        "elevationM": None,
        "condition": "Data unavailable — set OPENWEATHER_API_KEY",
        "forecast": [{"day": d, "tempC": 16, "rainMm": 10, "humidityPct": 70} for d in days],
    }


def _cache_to_dict(entry: WeatherCache):
    return {
        "location": entry.location_name,
        "temperatureC": entry.temperature_c,
        "humidityPct": entry.humidity_pct,
        "rainfallMm": entry.rainfall_mm,
        "windKmh": entry.wind_kmh,
        "elevationM": entry.elevation_m,
        "condition": entry.condition,
        "forecast": json.loads(entry.forecast_json) if entry.forecast_json else [],
    }
