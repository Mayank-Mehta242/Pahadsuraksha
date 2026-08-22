"""
Trains the Random Forest landslide-risk classifier and saves it to
landslide_model.pkl for app/services/ml_service.py to load.

A REAL historical landslide dataset (e.g. from the Uttarakhand State
Disaster Management Authority, Bhukosh/GSI records, or NASA's Global
Landslide Catalog) should replace `generate_synthetic_dataset()` before
this goes anywhere near production — the synthetic data here exists only
so the full pipeline (train -> save -> serve -> predict) runs end-to-end
without requiring a licensed dataset up front.

Usage:
    python machine_learning/train_model.py
"""
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

RANDOM_STATE = 42
MODEL_PATH = os.path.join(os.path.dirname(__file__), "landslide_model.pkl")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")


def _risk_label(rainfall, humidity, slope, historical_incidents, elevation):
    """Ground-truth rule used only to LABEL the synthetic training data —
    the model itself learns a Random Forest boundary from these examples
    rather than reapplying this rule at inference time."""
    score = (
        0.34 * min(rainfall / 80, 1)
        + 0.16 * min(humidity / 100, 1)
        + 0.27 * min(slope / 60, 1)
        + 0.18 * min(historical_incidents / 8, 1)
        + 0.05 * min(elevation / 3000, 1)
    )
    noise = np.random.normal(0, 0.05)
    score += noise

    if score < 0.3:
        return "LOW"
    if score < 0.5:
        return "MEDIUM"
    if score < 0.7:
        return "HIGH"
    return "VERY HIGH"


def generate_synthetic_dataset(n=6000):
    rng = np.random.default_rng(RANDOM_STATE)
    rainfall = rng.gamma(shape=2.0, scale=15, size=n)  # skewed toward lower rainfall, occasional heavy events
    humidity = rng.uniform(30, 100, size=n)
    temperature = rng.uniform(2, 30, size=n)
    elevation = rng.uniform(300, 3800, size=n)
    slope = rng.uniform(0, 60, size=n)
    historical_incidents = rng.poisson(lam=1.5, size=n)

    labels = [
        _risk_label(r, h, s, hi, e)
        for r, h, s, hi, e in zip(rainfall, humidity, slope, historical_incidents, elevation)
    ]

    df = pd.DataFrame(
        {
            "rainfall": rainfall.round(1),
            "humidity": humidity.round(1),
            "temperature": temperature.round(1),
            "elevation": elevation.round(0),
            "slope": slope.round(1),
            "historicalIncidents": historical_incidents,
            "riskLevel": labels,
        }
    )
    return df


def train():
    if os.path.exists(DATASET_PATH):
        print(f"Loading existing dataset from {DATASET_PATH}")
        df = pd.read_csv(DATASET_PATH)
    else:
        print("No dataset.csv found — generating a synthetic dataset (replace with real records for production).")
        df = generate_synthetic_dataset()
        df.to_csv(DATASET_PATH, index=False)
        print(f"Synthetic dataset saved to {DATASET_PATH}")

    feature_cols = ["rainfall", "humidity", "temperature", "elevation", "slope", "historicalIncidents"]
    X = df[feature_cols]
    y = df["riskLevel"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=4,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("Accuracy:", round(accuracy_score(y_test, preds) * 100, 2), "%")
    print(classification_report(y_test, preds))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()
