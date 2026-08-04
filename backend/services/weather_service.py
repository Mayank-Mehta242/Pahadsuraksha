import requests

from config import Config

# =====================================================
# OpenWeather API URLs
# =====================================================

CURRENT_WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

FORECAST_URL = (
    "https://api.openweathermap.org/data/2.5/forecast"
)

AIR_POLLUTION_URL = (
    "https://api.openweathermap.org/data/2.5/air_pollution"
)

GEOCODING_URL = (
    "http://api.openweathermap.org/geo/1.0/direct"
)


# =====================================================
# Weather Service
# =====================================================

class WeatherService:

    def __init__(self):

        self.api_key = Config.OPENWEATHER_API_KEY


    # =================================================
    # Get Coordinates
    #
    # Example:
    #
    # Dehradun
    #
    # ->
    #
    # Latitude
    # Longitude
    # =================================================

    def get_coordinates(self, city):

        params = {

            "q": city,

            "limit": 1,

            "appid": self.api_key

        }

        response = requests.get(

            GEOCODING_URL,

            params=params

        )

        if response.status_code != 200:

            return None

        data = response.json()

        if len(data) == 0:

            return None

        return {

            "city": data[0]["name"],

            "latitude": data[0]["lat"],

            "longitude": data[0]["lon"],

            "country": data[0]["country"]

        }


    # =================================================
    # Current Weather
    # =================================================

    def current_weather(self, latitude, longitude):

        params = {

            "lat": latitude,

            "lon": longitude,

            "appid": self.api_key,

            "units": "metric"

        }

        response = requests.get(

            CURRENT_WEATHER_URL,

            params=params

        )

        if response.status_code != 200:

            return None

        weather = response.json()

        rainfall = 0

        if "rain" in weather:

            rainfall = weather["rain"].get(

                "1h",

                0

            )

        return {

            "condition":

                weather["weather"][0]["main"],

            "description":

                weather["weather"][0]["description"],

            "icon":

                weather["weather"][0]["icon"],

            "temperature":

                weather["main"]["temp"],

            "feels_like":

                weather["main"]["feels_like"],

            "humidity":

                weather["main"]["humidity"],

            "pressure":

                weather["main"]["pressure"],

            "visibility":

                weather["visibility"],

            "wind_speed":

                weather["wind"]["speed"],

            "wind_degree":

                weather["wind"]["deg"],

            "clouds":

                weather["clouds"]["all"],

            "rainfall":

                rainfall,

            "sunrise":

                weather["sys"]["sunrise"],

            "sunset":

                weather["sys"]["sunset"],

            "city":

                weather["name"]

        }
        # =================================================
    # 5-Day / 3-Hour Forecast
    #
    # Used for:
    # • Hourly Forecast
    # • 7-Day Forecast
    # =================================================

    def weather_forecast(self, latitude, longitude):

        params = {

            "lat": latitude,

            "lon": longitude,

            "appid": self.api_key,

            "units": "metric"

        }

        response = requests.get(

            FORECAST_URL,

            params=params

        )

        if response.status_code != 200:

            return None

        return response.json()


    # =================================================
    # Hourly Forecast
    # =================================================

    def hourly_forecast(self, latitude, longitude):

        forecast = self.weather_forecast(

            latitude,

            longitude

        )

        if forecast is None:

            return []

        hourly = []

        for item in forecast["list"][:8]:

            rainfall = 0

            if "rain" in item:

                rainfall = item["rain"].get(

                    "3h",

                    0

                )

            hourly.append({

                "time":

                    item["dt_txt"],

                "temperature":

                    item["main"]["temp"],

                "condition":

                    item["weather"][0]["main"],

                "description":

                    item["weather"][0]["description"],

                "icon":

                    item["weather"][0]["icon"],

                "humidity":

                    item["main"]["humidity"],

                "wind_speed":

                    item["wind"]["speed"],

                "rainfall":

                    rainfall

            })

        return hourly


    # =================================================
    # Daily Forecast
    #
    # Returns one forecast for each day
    # =================================================

    def daily_forecast(self, latitude, longitude):

        forecast = self.weather_forecast(

            latitude,

            longitude

        )

        if forecast is None:

            return []

        daily = []

        added_dates = set()

        for item in forecast["list"]:

            date = item["dt_txt"].split()[0]

            if date in added_dates:

                continue

            added_dates.add(date)

            rainfall = 0

            if "rain" in item:

                rainfall = item["rain"].get(

                    "3h",

                    0

                )

            daily.append({

                "date": date,

                "temperature":

                    item["main"]["temp"],

                "condition":

                    item["weather"][0]["main"],

                "description":

                    item["weather"][0]["description"],

                "icon":

                    item["weather"][0]["icon"],

                "humidity":

                    item["main"]["humidity"],

                "wind_speed":

                    item["wind"]["speed"],

                "rainfall":

                    rainfall

            })

        return daily


    # =================================================
    # Air Quality Index (AQI)
    # =================================================

    def air_quality(self, latitude, longitude):

        params = {

            "lat": latitude,

            "lon": longitude,

            "appid": self.api_key

        }

        response = requests.get(

            AIR_POLLUTION_URL,

            params=params

        )

        if response.status_code != 200:

            return None

        data = response.json()

        air = data["list"][0]

        return {

            "aqi":

                air["main"]["aqi"],

            "co":

                air["components"]["co"],

            "no":

                air["components"]["no"],

            "no2":

                air["components"]["no2"],

            "o3":

                air["components"]["o3"],

            "so2":

                air["components"]["so2"],

            "pm2_5":

                air["components"]["pm2_5"],

            "pm10":

                air["components"]["pm10"]

        }


    # =================================================
    # Weather Alerts
    #
    # Placeholder
    #
    # Replace later using One Call API
    # or IMD Alerts API
    # =================================================

    def weather_alerts(self):

        return [

            {

                "title": "No Active Alerts",

                "description":
                    "Weather conditions are normal."

            }

        ]
      # =================================================
    # UV Index
    #
    # Note:
    # OpenWeather One Call API provides UV Index.
    # If unavailable on your plan, this function
    # returns None.
    # =================================================

    def uv_index(self, latitude, longitude):

        ONECALL_URL = (
            "https://api.openweathermap.org/data/3.0/onecall"
        )

        params = {

            "lat": latitude,

            "lon": longitude,

            "exclude": "minutely,hourly,daily,alerts",

            "appid": self.api_key,

            "units": "metric"

        }

        response = requests.get(

            ONECALL_URL,

            params=params

        )

        if response.status_code != 200:

            return None

        data = response.json()

        return data["current"].get(

            "uvi",

            None

        )


    # =================================================
    # Route Weather
    #
    # Currently fetches weather for:
    # Source
    # Destination
    #
    # Future:
    # Sample weather every 5–10 km along the route.
    # =================================================

    def route_weather(self, source, destination):

        source_weather = self.current_weather(

            source["latitude"],

            source["longitude"]

        )

        destination_weather = self.current_weather(

            destination["latitude"],

            destination["longitude"]

        )

        return {

            "source": source_weather,

            "destination": destination_weather

        }


    # =================================================
    # Road Safety Status
    # =================================================

    def road_safety(self, weather):

        rainfall = weather["rainfall"]

        wind = weather["wind_speed"]

        visibility = weather["visibility"]

        if rainfall >= 50:

            return "High Landslide Risk"

        if rainfall >= 20:

            return "Risky"

        if rainfall >= 5:

            return "Moderate"

        if wind >= 18:

            return "Moderate"

        if visibility <= 1000:

            return "Moderate"

        return "Safe"


    # =================================================
    # AI Landslide Risk
    #
    # Temporary Rule-Based Logic
    #
    # Replace later with:
    # Random Forest Model
    # =================================================

    def landslide_risk(self, weather):

        rainfall = weather["rainfall"]

        humidity = weather["humidity"]

        wind = weather["wind_speed"]

        if rainfall >= 60:

            return "High"

        elif rainfall >= 30:

            return "Medium"

        elif humidity >= 90 and wind >= 15:

            return "Medium"

        else:

            return "Low"


    # =================================================
    # Travel Recommendation
    # =================================================

    def recommendation(self, risk):

        recommendations = {

            "Low": "Safe Journey",

            "Medium": "Travel with Caution",

            "High": "Avoid Non-Essential Travel"

        }

        return recommendations.get(

            risk,

            "No Recommendation"

        )


    # =================================================
    # Complete Weather Summary
    #
    # Used by Dashboard and Prediction API
    # =================================================

    def weather_summary(self, city):

        location = self.get_coordinates(city)

        if location is None:

            return None

        weather = self.current_weather(

            location["latitude"],

            location["longitude"]

        )

        if weather is None:

            return None

        return {

            "location": location,

            "weather": weather,

            "road_status": self.road_safety(

                weather

            ),

            "landslide_risk": self.landslide_risk(

                weather

            ),

            "recommendation": self.recommendation(

                self.landslide_risk(weather)

            ),

            "hourly_forecast": self.hourly_forecast(

                location["latitude"],

                location["longitude"]

            ),

            "daily_forecast": self.daily_forecast(

                location["latitude"],

                location["longitude"]

            ),

            "air_quality": self.air_quality(

                location["latitude"],

                location["longitude"]

            ),

            "uv_index": self.uv_index(

                location["latitude"],

                location["longitude"]

            ),

            "alerts": self.weather_alerts()

        }
         # =================================================
    # Complete Route Analysis
    #
    # Used by AI Prediction API
    # =================================================

    def analyze_route(self, source_city, destination_city):

        source = self.get_coordinates(source_city)

        destination = self.get_coordinates(destination_city)

        if source is None or destination is None:

            return {

                "success": False,

                "message": "Invalid Source or Destination."

            }

        route_weather = self.route_weather(

            source,

            destination

        )

        source_weather = route_weather["source"]

        destination_weather = route_weather["destination"]

        source_risk = self.landslide_risk(

            source_weather

        )

        destination_risk = self.landslide_risk(

            destination_weather

        )

        # --------------------------------------------
        # Overall Route Risk
        # --------------------------------------------

        risk_order = {

            "Low": 1,

            "Medium": 2,

            "High": 3

        }

        overall_risk = source_risk

        if risk_order[destination_risk] > risk_order[source_risk]:

            overall_risk = destination_risk

        return {

            "success": True,

            "source": source,

            "destination": destination,

            "source_weather": source_weather,

            "destination_weather": destination_weather,

            "overall_risk": overall_risk,

            "recommendation": self.recommendation(

                overall_risk

            )

        }


    # =================================================
    # Health Check
    #
    # Test API Connection
    # =================================================

    def health_check(self):

        try:

            weather = self.weather_summary(

                "Tehri"

            )

            if weather is None:

                return {

                    "status": False,

                    "message": "Weather Service Unavailable"

                }

            return {

                "status": True,

                "message": "Weather Service Running"

            }

        except Exception as e:

            return {

                "status": False,

                "message": str(e)

            }


# =====================================================
# Singleton Instance
#
# Import this everywhere
# =====================================================

weather_service = WeatherService()


# =====================================================
# Utility Functions
# =====================================================

def get_weather(city):

    return weather_service.weather_summary(city)


def get_route_weather(source, destination):

    return weather_service.analyze_route(

        source,

        destination

    )


def get_current_weather(city):

    location = weather_service.get_coordinates(city)

    if location is None:

        return None

    return weather_service.current_weather(

        location["latitude"],

        location["longitude"]

    )


def get_hourly_forecast(city):

    location = weather_service.get_coordinates(city)

    if location is None:

        return []

    return weather_service.hourly_forecast(

        location["latitude"],

        location["longitude"]

    )


def get_daily_forecast(city):

    location = weather_service.get_coordinates(city)

    if location is None:

        return []

    return weather_service.daily_forecast(

        location["latitude"],

        location["longitude"]

    )


def get_air_quality(city):

    location = weather_service.get_coordinates(city)

    if location is None:

        return None

    return weather_service.air_quality(

        location["latitude"],

        location["longitude"]

    )


def get_uv_index(city):

    location = weather_service.get_coordinates(city)

    if location is None:

        return None

    return weather_service.uv_index(

        location["latitude"],

        location["longitude"]

    ) 