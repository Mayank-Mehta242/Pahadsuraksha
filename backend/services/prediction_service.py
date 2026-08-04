import os
import joblib
import numpy as np

from config import Config


# =====================================================
# Prediction Service
# =====================================================

class PredictionService:

    def __init__(self):

        self.model = None

        self.model_path = os.path.join(

            Config.MODEL_FOLDER,

            "model.pkl"

        )

        self.load_model()


    # =================================================
    # Load AI Model
    # =================================================

    def load_model(self):

        try:

            self.model = joblib.load(

                self.model_path

            )

            print(

                "AI Model Loaded Successfully."

            )

        except Exception:

            self.model = None

            print(

                "Model not found. Prediction service running in fallback mode."

            )


    # =================================================
    # Check Model Status
    # =================================================

    def model_loaded(self):

        return self.model is not None


    # =================================================
    # Prepare Features
    #
    # Input:
    #
    # rainfall
    # humidity
    # temperature
    # wind_speed
    # pressure
    # visibility
    #
    # Output:
    # NumPy Array
    # =================================================

    def prepare_features(

        self,

        rainfall,

        humidity,

        temperature,

        wind_speed,

        pressure,

        visibility

    ):

        features = np.array([

            rainfall,

            humidity,

            temperature,

            wind_speed,

            pressure,

            visibility

        ])

        return features.reshape(

            1,

            -1

        )


    # =================================================
    # Prepare Weather Dictionary
    # =================================================

    def prepare_weather(self, weather):

        return self.prepare_features(

            weather["rainfall"],

            weather["humidity"],

            weather["temperature"],

            weather["wind_speed"],

            weather["pressure"],

            weather["visibility"]

        )


    # =================================================
    # Rule-Based Prediction
    #
    # Used only if model.pkl
    # is unavailable.
    # =================================================

    def fallback_prediction(

        self,

        weather

    ):

        rainfall = weather["rainfall"]

        humidity = weather["humidity"]

        wind = weather["wind_speed"]

        if rainfall >= 60:

            return 2

        elif rainfall >= 30:

            return 1

        elif humidity >= 90 and wind >= 15:

            return 1

        return 0
        # =================================================
    # AI Prediction
    #
    # Returns:
    # 0 -> Low
    # 1 -> Medium
    # 2 -> High
    # =================================================

    def predict(self, weather):

        # ---------------------------------------------
        # Prepare Features
        # ---------------------------------------------

        features = self.prepare_weather(

            weather

        )

        # ---------------------------------------------
        # Fallback Mode
        # ---------------------------------------------

        if self.model is None:

            prediction = self.fallback_prediction(

                weather

            )

            confidence = 70.0

            return {

                "prediction": prediction,

                "confidence": confidence,

                "mode": "Fallback"

            }

        # ---------------------------------------------
        # AI Prediction
        # ---------------------------------------------

        prediction = int(

            self.model.predict(

                features

            )[0]

        )

        confidence = self.calculate_confidence(

            features

        )

        return {

            "prediction": prediction,

            "confidence": confidence,

            "mode": "AI"

        }


    # =================================================
    # Confidence Score
    #
    # Uses predict_proba()
    # =================================================

    def calculate_confidence(

        self,

        features

    ):

        try:

            probabilities = self.model.predict_proba(

                features

            )[0]

            confidence = max(

                probabilities

            ) * 100

            return round(

                confidence,

                2

            )

        except Exception:

            return 80.0


    # =================================================
    # Risk Level Mapping
    # =================================================

    def risk_level(

        self,

        prediction

    ):

        mapping = {

            0: "Low",

            1: "Medium",

            2: "High"

        }

        return mapping.get(

            prediction,

            "Unknown"

        )


    # =================================================
    # Risk Color
    #
    # Useful for React UI
    # =================================================

    def risk_color(

        self,

        prediction

    ):

        colors = {

            0: "#28a745",

            1: "#f0ad4e",

            2: "#dc3545"

        }

        return colors.get(

            prediction,

            "#6c757d"

        )


    # =================================================
    # Prediction Result
    #
    # Converts raw model output
    # into frontend-friendly JSON
    # =================================================

    def prediction_result(

        self,

        weather

    ):

        result = self.predict(

            weather

        )

        return {

            "risk":

                self.risk_level(

                    result["prediction"]

                ),

            "confidence":

                result["confidence"],

            "color":

                self.risk_color(

                    result["prediction"]

                ),

            "prediction_mode":

                result["mode"]

        }
        # =================================================
    # Travel Recommendation
    # =================================================

    def recommendation(self, risk):

        recommendations = {

            "Low": {

                "status": "Safe Journey",

                "message":
                    "Weather conditions are favorable. Travel is considered safe."

            },

            "Medium": {

                "status": "Travel with Caution",

                "message":
                    "Drive carefully. Moderate rainfall or slippery roads may be present."

            },

            "High": {

                "status": "Avoid Travel",

                "message":
                    "High probability of landslides. Avoid unnecessary travel."

            }

        }

        return recommendations.get(

            risk,

            {

                "status": "Unknown",

                "message": "No recommendation available."

            }

        )


    # =================================================
    # Route Prediction
    #
    # WeatherService provides:
    # Source Weather
    # Destination Weather
    #
    # Overall prediction is based on
    # the higher risk location.
    # =================================================

    def route_prediction(

        self,

        source_weather,

        destination_weather

    ):

        source_result = self.prediction_result(

            source_weather

        )

        destination_result = self.prediction_result(

            destination_weather

        )

        priority = {

            "Low": 1,

            "Medium": 2,

            "High": 3

        }

        overall = source_result

        if priority[

            destination_result["risk"]

        ] > priority[

            source_result["risk"]

        ]:

            overall = destination_result

        recommendation = self.recommendation(

            overall["risk"]

        )

        return {

            "source": source_result,

            "destination": destination_result,

            "overallRisk":

                overall["risk"],

            "confidence":

                overall["confidence"],

            "recommendation":

                recommendation["status"],

            "message":

                recommendation["message"]

        }


    # =================================================
    # Prediction Summary
    #
    # Used by Dashboard &
    # Prediction API
    # =================================================

    def prediction_summary(

        self,

        weather,

        source,

        destination

    ):

        result = self.prediction_result(

            weather

        )

        recommendation = self.recommendation(

            result["risk"]

        )

        return {

            "source":

                source,

            "destination":

                destination,

            "weather": {

                "temperature":

                    weather["temperature"],

                "humidity":

                    weather["humidity"],

                "rainfall":

                    weather["rainfall"],

                "wind_speed":

                    weather["wind_speed"],

                "pressure":

                    weather["pressure"],

                "visibility":

                    weather["visibility"]

            },

            "prediction": {

                "risk":

                    result["risk"],

                "confidence":

                    result["confidence"],

                "color":

                    result["color"],

                "mode":

                    result["prediction_mode"]

            },

            "travel": {

                "status":

                    recommendation["status"],

                "message":

                    recommendation["message"]

            }

        }


    # =================================================
    # Model Information
    #
    # Useful for Admin Panel
    # =================================================

    def model_information(self):

        return {

            "model_loaded":

                self.model_loaded(),

            "model_path":

                self.model_path,

            "prediction_classes": [

                "Low",

                "Medium",

                "High"

            ]

        }
    # =====================================================
# Health Check
#
# Used by Admin Dashboard
# =====================================================

    def health_check(self):

        return {

            "service": "Prediction Service",

            "status": "Running",

            "model_loaded": self.model_loaded(),

            "model_path": self.model_path

        }


    # =================================================
    # Reload Model
    #
    # Useful after training a new model
    # =================================================

    def reload_model(self):

        self.load_model()

        return {

            "success": True,

            "message": "AI model reloaded successfully.",

            "model_loaded": self.model_loaded()

        }


    # =================================================
    # Predict From Route
    #
    # Used by Prediction API
    #
    # Input:
    #   source_weather
    #   destination_weather
    #
    # Output:
    #   Complete Route Prediction
    # =================================================

    def predict_route(

        self,

        source_weather,

        destination_weather

    ):

        return self.route_prediction(

            source_weather,

            destination_weather

        )


# =====================================================
# Singleton Instance
#
# Import this everywhere
# =====================================================

prediction_service = PredictionService()


# =====================================================
# Utility Functions
# =====================================================

def predict(weather):

    return prediction_service.prediction_result(

        weather

    )


def predict_route(

    source_weather,

    destination_weather

):

    return prediction_service.predict_route(

        source_weather,

        destination_weather

    )


def prediction_summary(

    weather,

    source,

    destination

):

    return prediction_service.prediction_summary(

        weather,

        source,

        destination

    )


def prediction_health():

    return prediction_service.health_check()


def reload_prediction_model():

    return prediction_service.reload_model()


# =====================================================
# Demo Function
#
# Used while testing backend
# =====================================================

def test_prediction():

    sample_weather = {

        "rainfall": 22,

        "humidity": 88,

        "temperature": 19,

        "wind_speed": 12,

        "pressure": 1008,

        "visibility": 3500

    }

    return prediction_service.prediction_summary(

        sample_weather,

        "Dehradun",

        "Mussoorie"

    )