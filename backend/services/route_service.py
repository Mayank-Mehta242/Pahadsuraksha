import requests

from config import Config

# =====================================================
# OpenRouteService API URLs
# =====================================================

GEOCODE_URL = (
    "https://api.openrouteservice.org/geocode/search"
)

DIRECTIONS_URL = (
    "https://api.openrouteservice.org/v2/directions/driving-car"
)


# =====================================================
# Route Service
# =====================================================

class RouteService:

    def __init__(self):

        self.api_key = Config.OPENROUTESERVICE_API_KEY


    # =================================================
    # Request Headers
    # =================================================

    def headers(self):

        return {

            "Authorization": self.api_key,

            "Content-Type": "application/json"

        }


    # =================================================
    # Convert City -> Coordinates
    #
    # Example
    #
    # Dehradun
    #
    # ->
    #
    # Latitude
    # Longitude
    # =================================================

    def get_coordinates(self, location):

        params = {

            "text": location,

            "size": 1

        }

        response = requests.get(

            GEOCODE_URL,

            headers=self.headers(),

            params=params

        )

        if response.status_code != 200:

            return None

        data = response.json()

        if len(data["features"]) == 0:

            return None

        coordinates = data["features"][0]["geometry"]["coordinates"]

        properties = data["features"][0]["properties"]

        return {

            "name": properties.get(

                "label",

                location

            ),

            "latitude": coordinates[1],

            "longitude": coordinates[0]

        }


    # =================================================
    # Validate Route Locations
    # =================================================

    def validate_locations(

        self,

        source,

        destination

    ):

        source_location = self.get_coordinates(

            source

        )

        destination_location = self.get_coordinates(

            destination

        )

        if source_location is None:

            return {

                "success": False,

                "message": "Invalid source location."

            }

        if destination_location is None:

            return {

                "success": False,

                "message": "Invalid destination location."

            }

        return {

            "success": True,

            "source": source_location,

            "destination": destination_location

        }


    # =================================================
    # Distance Between Two Coordinates
    #
    # (Approximation using Haversine Formula)
    #
    # Used if Route API is unavailable
    # =================================================

    def haversine_distance(

        self,

        lat1,

        lon1,

        lat2,

        lon2

    ):

        from math import radians
        from math import sin
        from math import cos
        from math import sqrt
        from math import atan2

        radius = 6371

        dlat = radians(

            lat2 - lat1

        )

        dlon = radians(

            lon2 - lon1

        )

        a = (

            sin(dlat / 2) ** 2 +

            cos(radians(lat1))

            *

            cos(radians(lat2))

            *

            sin(dlon / 2) ** 2

        )

        c = 2 * atan2(

            sqrt(a),

            sqrt(1 - a)

        )

        return round(

            radius * c,

            2

        )
        # =================================================
    # Get Route
    #
    # Returns:
    # Distance
    # Duration
    # Geometry
    # =================================================

    def get_route(self, source, destination):

        validation = self.validate_locations(

            source,

            destination

        )

        if validation["success"] is False:

            return validation

        source_location = validation["source"]

        destination_location = validation["destination"]

        body = {

            "coordinates": [

                [

                    source_location["longitude"],

                    source_location["latitude"]

                ],

                [

                    destination_location["longitude"],

                    destination_location["latitude"]

                ]

            ]

        }

        response = requests.post(

            DIRECTIONS_URL,

            headers=self.headers(),

            json=body

        )

        if response.status_code != 200:

            return {

                "success": False,

                "message": "Unable to generate route."

            }

        data = response.json()

        route = data["routes"][0]

        summary = route["summary"]

        geometry = route["geometry"]

        return {

            "success": True,

            "source": source_location,

            "destination": destination_location,

            "distance_km": round(

                summary["distance"] / 1000,

                2

            ),

            "duration_minutes": round(

                summary["duration"] / 60,

                2

            ),

            "geometry": geometry

        }


    # =================================================
    # Format Travel Time
    #
    # Example
    #
    # 142 Minutes
    #
    # ->
    #
    # 2 hr 22 min
    # =================================================

    def format_duration(self, minutes):

        hours = int(minutes // 60)

        mins = int(minutes % 60)

        if hours == 0:

            return f"{mins} min"

        return f"{hours} hr {mins} min"


    # =================================================
    # Route Summary
    #
    # Ready for React Dashboard
    # =================================================

    def route_summary(self, source, destination):

        route = self.get_route(

            source,

            destination

        )

        if route["success"] is False:

            return route

        return {

            "success": True,

            "source": route["source"]["name"],

            "destination": route["destination"]["name"],

            "distance": route["distance_km"],

            "estimated_time":

                self.format_duration(

                    route["duration_minutes"]

                ),

            "geometry": route["geometry"]

        }


    # =================================================
    # Decode Route
    #
    # Placeholder
    #
    # Later:
    # Convert encoded geometry into
    # latitude-longitude coordinates
    # for Leaflet.
    # =================================================

    def decode_geometry(self, geometry):

        return geometry
        # =================================================
    # Sample Route Points
    #
    # Used for:
    # - Weather sampling
    # - AI prediction
    # - Future elevation analysis
    #
    # Currently:
    # Returns Source + Destination.
    #
    # Future:
    # Decode geometry and return
    # points every 5–10 km.
    # =================================================

    def sample_route_points(self, source, destination):

        route = self.get_route(

            source,

            destination

        )

        if route["success"] is False:

            return route

        points = [

            {

                "name": "Source",

                "latitude":
                    route["source"]["latitude"],

                "longitude":
                    route["source"]["longitude"]

            },

            {

                "name": "Destination",

                "latitude":
                    route["destination"]["latitude"],

                "longitude":
                    route["destination"]["longitude"]

            }

        ]

        return {

            "success": True,

            "points": points

        }


    # =================================================
    # Bounding Box
    #
    # Useful for:
    # Leaflet
    # Map Zoom
    # Future GIS Features
    # =================================================

    def bounding_box(self, source, destination):

        route = self.get_route(

            source,

            destination

        )

        if route["success"] is False:

            return route

        latitudes = [

            route["source"]["latitude"],

            route["destination"]["latitude"]

        ]

        longitudes = [

            route["source"]["longitude"],

            route["destination"]["longitude"]

        ]

        return {

            "success": True,

            "min_lat": min(latitudes),

            "max_lat": max(latitudes),

            "min_lon": min(longitudes),

            "max_lon": max(longitudes)

        }


    # =================================================
    # Elevation Placeholder
    #
    # Future:
    # OpenTopography API
    #
    # Returns elevation profile.
    # =================================================

    def elevation_profile(self, source, destination):

        return {

            "success": True,

            "message":

                "Elevation service not integrated yet.",

            "profile": []

        }


    # =================================================
    # Complete Route Analysis
    #
    # Used by Dashboard
    # Prediction API
    # Weather API
    # =================================================

    def analyze_route(self, source, destination):

        route = self.get_route(

            source,

            destination

        )

        if route["success"] is False:

            return route

        samples = self.sample_route_points(

            source,

            destination

        )

        bbox = self.bounding_box(

            source,

            destination

        )

        elevation = self.elevation_profile(

            source,

            destination

        )

        return {

            "success": True,

            "route": {

                "source":

                    route["source"],

                "destination":

                    route["destination"],

                "distance":

                    route["distance_km"],

                "duration":

                    self.format_duration(

                        route["duration_minutes"]

                    ),

                "geometry":

                    route["geometry"]

            },

            "sample_points":

                samples["points"],

            "bounding_box":

                bbox,

            "elevation":

                elevation

        }


    # =================================================
    # Route Health Check
    #
    # Tests OpenRouteService
    # =================================================

    def health_check(self):

        test = self.get_coordinates(

            "Dehradun"

        )

        if test is None:

            return {

                "status": False,

                "message":

                    "OpenRouteService unavailable."

            }

        return {

            "status": True,

            "message":

                "Route Service Running."

        }
    # =====================================================
# Singleton Instance
#
# Import this everywhere
# =====================================================

route_service = RouteService()


# =====================================================
# Utility Functions
#
# These functions allow the rest of the backend
# to use the service without creating an object.
# =====================================================

def get_coordinates(location):

    return route_service.get_coordinates(

        location

    )


def get_route(source, destination):

    return route_service.get_route(

        source,

        destination

    )


def get_route_summary(source, destination):

    return route_service.route_summary(

        source,

        destination

    )


def get_route_analysis(source, destination):

    return route_service.analyze_route(

        source,

        destination

    )


def get_sample_points(source, destination):

    result = route_service.sample_route_points(

        source,

        destination

    )

    if result["success"] is False:

        return []

    return result["points"]


def get_bounding_box(source, destination):

    return route_service.bounding_box(

        source,

        destination

    )


def get_elevation_profile(source, destination):

    return route_service.elevation_profile(

        source,

        destination

    )


def route_health():

    return route_service.health_check()


# =====================================================
# Demo Function
#
# Useful while testing the backend
#
# Example:
#
# print(test_route())
# =====================================================

def test_route():

    return route_service.route_summary(

        "Dehradun",

        "Mussoorie"

    )