from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

from app.extensions import db
from app.models.prediction import Prediction
from app.services.ml_service import predict_risk, FEATURE_ORDER

predict_bp = Blueprint("predict", __name__, url_prefix="/api/predict")


@predict_bp.post("")
def predict():
    body = request.get_json(silent=True) or {}
    missing = [f for f in FEATURE_ORDER if body.get(f) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        inputs = {f: float(body[f]) for f in FEATURE_ORDER}
    except (TypeError, ValueError):
        return jsonify({"error": "All fields must be numeric."}), 400

    try:
        result = predict_risk(inputs)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 503

    # Log the prediction if the caller is authenticated; anonymous/guest
    # predictions (from the public dashboard) are allowed and just skip this.
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except Exception:
        pass

    entry = Prediction(
        user_id=user_id,
        rainfall=inputs["rainfall"],
        humidity=inputs["humidity"],
        temperature=inputs["temperature"],
        elevation=inputs["elevation"],
        slope=inputs["slope"],
        historical_incidents=inputs["historicalIncidents"],
        risk_level=result["riskLevel"],
        confidence=result["confidence"],
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify(result), 200
