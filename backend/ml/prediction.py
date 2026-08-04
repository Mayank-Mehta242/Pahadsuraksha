import os
import joblib
import numpy as np

from config import Config


# =====================================================
# Landslide Prediction Model
# =====================================================

class LandslidePredictionModel:

    def __init__(self):

        self.model = None

        self.model_path = os.path.join(

            Config.MODEL_FOLDER,

            "model.pkl"

        )

        self.load_model()


    # =================================================
    # Load Trained Model
    # =================================================

    def load_model(self):

        try:

            self.model = joblib.load(

                self.model_path

            )

            print(

                "Landslide Prediction Model Loaded."

            )

        except Exception as e:

            self.model = None

            print(

                f"Unable to load model: {e}"

            )


    # =================================================
    # Check Model Status
    # =================================================

    def is_loaded(self):

        return self.model is not None


    # =================================================
    # Feature Preparation
    #
    # Order must match training dataset
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
    # Weather Dictionary
    # -> NumPy Features
    # =================================================

    def weather_to_features(

        self,

        weather

    ):

        return self.prepare_features(

            weather["rainfall"],

            weather["humidity"],

            weather["temperature"],

            weather["wind_speed"],

            weather["pressure"],

            weather["visibility"]

        )


    # =================================================
    # Default Rule-Based Prediction
    #
    # Used if ML model is unavailable
    # =================================================

    def fallback_prediction(

        self,

        weather

    ):

        rainfall = weather["rainfall"]

        humidity = weather["humidity"]

        wind_speed = weather["wind_speed"]

        if rainfall >= 60:

            return 2

        elif rainfall >= 30:

            return 1

        elif humidity >= 90 and wind_speed >= 15:

            return 1

        return 0
        # =================================================
    # Predict Risk
    #
    # Returns:
    # 0 -> Low
    # 1 -> Medium
    # 2 -> High
    # =================================================

    def predict(self, weather):

        features = self.weather_to_features(

            weather

        )

        # ---------------------------------------------
        # Fallback Prediction
        # ---------------------------------------------

        if not self.is_loaded():

            prediction = self.fallback_prediction(

                weather

            )

            return {

                "prediction": prediction,

                "confidence": 70.0,

                "mode": "Fallback"

            }

        # ---------------------------------------------
        # Machine Learning Prediction
        # ---------------------------------------------

        prediction = int(

            self.model.predict(

                features

            )[0]

        )

        confidence = self.predict_confidence(

            features

        )

        return {

            "prediction": prediction,

            "confidence": confidence,

            "mode": "AI"

        }


    # =================================================
    # Prediction Confidence
    #
    # Uses predict_proba()
    # =================================================

    def predict_confidence(

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
    # Useful for Dashboard UI
    # =================================================

    def risk_color(

        self,

        prediction

    ):

        colors = {

            0: "#28a745",

            1: "#ffc107",

            2: "#dc3545"

        }

        return colors.get(

            prediction,

            "#6c757d"

        )


    # =================================================
    # Prediction Result
    #
    # Converts model output into
    # frontend-friendly JSON
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

            "mode":

                result["mode"]

        }
        # =================================================
    # Travel Recommendation
    # =================================================

    def recommendation(

        self,

        risk

    ):

        recommendations = {

            "Low": {

                "status": "Safe",

                "message":

                    "Travel conditions are safe."

            },

            "Medium": {

                "status": "Caution",

                "message":

                    "Drive carefully. Moderate landslide risk."

            },

            "High": {

                "status": "Danger",

                "message":

                    "Avoid travel. High landslide probability."

            }

        }

        return recommendations.get(

            risk,

            {

                "status": "Unknown",

                "message":

                    "Recommendation unavailable."

            }

        )


    # =================================================
    # Complete Prediction Summary
    # =================================================

    def prediction_summary(

        self,

        weather

    ):

        prediction = self.prediction_result(

            weather

        )

        recommendation = self.recommendation(

            prediction["risk"]

        )

        return {

            "weather": weather,

            "prediction": {

                "risk":

                    prediction["risk"],

                "confidence":

                    prediction["confidence"],

                "color":

                    prediction["color"],

                "mode":

                    prediction["mode"]

            },

            "recommendation":

                recommendation

        }


    # =================================================
    # Batch Prediction
    #
    # Predicts multiple weather records.
    # =================================================

    def batch_prediction(

        self,

        weather_list

    ):

        results = []

        for weather in weather_list:

            results.append(

                self.prediction_summary(

                    weather

                )

            )

        return results


    # =================================================
    # Model Metadata
    #
    # Useful for Admin Dashboard
    # =================================================

    def model_information(self):

        return {

            "model_loaded":

                self.is_loaded(),

            "model_path":

                self.model_path,

            "prediction_classes": [

                "Low",

                "Medium",

                "High"

            ],

            "input_features": [

                "rainfall",

                "humidity",

                "temperature",

                "wind_speed",

                "pressure",

                "visibility"

            ]

        }


    # =================================================
    # Example Weather Sample
    #
    # Useful for testing
    # =================================================

    def sample_weather(self):

        return {

            "rainfall": 28,

            "humidity": 85,

            "temperature": 19,

            "wind_speed": 12,

            "pressure": 1009,

            "visibility": 4500

        }
    # =====================================================
# Health Check
# =====================================================

    def health_check(self):

        return {

            "service": "Landslide Prediction Model",

            "status": "Running",

            "model_loaded": self.is_loaded(),

            "model_path": self.model_path

        }


    # =================================================
    # Reload Model
    #
    # Used after training a new model
    # =================================================

    def reload_model(self):

        self.load_model()

        return {

            "success": True,

            "message": "Model reloaded successfully.",

            "model_loaded": self.is_loaded()

        }


# =====================================================
# Singleton Instance
# =====================================================

landslide_model = LandslidePredictionModel()


# =====================================================
# Utility Functions
# =====================================================

def predict(weather):

    return landslide_model.predict(

        weather

    )


def prediction_result(weather):

    return landslide_model.prediction_result(

        weather

    )


def prediction_summary(weather):

    return landslide_model.prediction_summary(

        weather

    )


def batch_prediction(weather_list):

    return landslide_model.batch_prediction(

        weather_list

    )


def recommendation(risk):

    return landslide_model.recommendation(

        risk

    )


def model_information():

    return landslide_model.model_information()


def model_health():

    return landslide_model.health_check()


def reload_model():

    return landslide_model.reload_model()


# =====================================================
# Demo Function
#
# Used while testing the model
# =====================================================

def test_prediction():

    sample = landslide_model.sample_weather()

    return landslide_model.prediction_summary(

        sample

    )


# =====================================================
# Run File Directly
#
# python ml/prediction.py
# =====================================================

if __name__ == "__main__":

    print("=" * 50)

    print("PAHADSURAKSHA AI Prediction Model")

    print("=" * 50)

    print()

    print("Health Check:")

    print(model_health())

    print()

    print("Sample Prediction:")

    print(test_prediction())
    