"""
Loads the trained Random Forest model (see machine_learning/train_model.py)
and turns a raw prediction into the explained shape the frontend expects:
{ riskLevel, confidence, reasons, factorWeights }
"""
import os
import joblib
import numpy as np
from flask import current_app

FEATURE_ORDER = ["rainfall", "humidity", "temperature", "elevation", "slope", "historicalIncidents"]
LABELS = ["LOW", "MEDIUM", "HIGH", "VERY HIGH"]

_model_cache = None


def _load_model():
    global _model_cache
    if _model_cache is None:
        path = current_app.config["ML_MODEL_PATH"]
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"No trained model found at {path}. Run `python machine_learning/train_model.py` first."
            )
        _model_cache = joblib.load(path)
    return _model_cache


def _reasons_for(inputs, risk_key):
    """Rule-based, human-readable explanations layered on top of the model's
    numeric output — the brief explicitly asks for "why", not just a label."""
    reasons = []
    if inputs["rainfall"] >= 40:
        reasons.append("Heavy rainfall over the last 48 hours")
    elif inputs["rainfall"] >= 15:
        reasons.append("Moderate rainfall accumulation in the area")

    if inputs["slope"] >= 35:
        reasons.append("Steep terrain (slope above 35°)")
    elif inputs["slope"] >= 20:
        reasons.append("Moderately steep terrain")

    if inputs["humidity"] >= 75:
        reasons.append("High soil saturation likely given elevated humidity")

    if inputs["historicalIncidents"] >= 3:
        reasons.append("Multiple historical landslides recorded nearby")
    elif inputs["historicalIncidents"] >= 1:
        reasons.append("At least one historical landslide recorded nearby")

    if inputs["elevation"] >= 1500:
        reasons.append("High elevation zone with typically looser soil cover")

    if not reasons:
        reasons.append("Conditions are currently within normal ranges for this area")

    return reasons


def predict_risk(inputs: dict):
    model = _load_model()
    ordered = np.array([[float(inputs[f]) for f in FEATURE_ORDER]])

    proba = model.predict_proba(ordered)[0]
    class_index = int(np.argmax(proba))
    risk_level = model.classes_[class_index] if hasattr(model, "classes_") else LABELS[class_index]
    confidence = round(float(proba[class_index]) * 100, 1)

    importances = getattr(model, "feature_importances_", None)
    if importances is None:
        importances = np.ones(len(FEATURE_ORDER)) / len(FEATURE_ORDER)

    factor_weights = [
        {"factor": _pretty_name(f), "weight": round(float(w), 3)}
        for f, w in sorted(zip(FEATURE_ORDER, importances), key=lambda x: x[1], reverse=True)
    ]

    return {
        "riskLevel": str(risk_level),
        "confidence": confidence,
        "reasons": _reasons_for(inputs, risk_level),
        "factorWeights": factor_weights,
    }


def _pretty_name(field):
    return {
        "rainfall": "Rainfall",
        "humidity": "Humidity",
        "temperature": "Temperature",
        "elevation": "Elevation",
        "slope": "Slope",
        "historicalIncidents": "Historical incidents",
    }.get(field, field)
