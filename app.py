"""
EdgeAI Monitor - Flask application.

Real-time embedded systems monitoring dashboard
with AI-powered anomaly detection.
"""

import os

from flask import Flask, jsonify, render_template

from sensor import SensorSimulator
from detector import AnomalyDetector

app = Flask(__name__)

# Initialize components
sensor = SensorSimulator()
detector = AnomalyDetector(contamination=0.05)

# Store history
history: list[dict] = []
MAX_HISTORY = 200
RETRAIN_AT = 50
has_trained = False


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/data")
def get_data():
    """Get latest sensor reading with anomaly score."""
    global has_trained

    reading = sensor.read()

    # Auto-train once we have enough real data
    if not has_trained and len(history) >= RETRAIN_AT:
        print(f"Auto-training model on {RETRAIN_AT} real readings...")
        detector.train(history[:RETRAIN_AT])
        has_trained = True
        print("Model trained on real system baseline.")

    result = detector.predict(reading)
    history.append(result)
    if len(history) > MAX_HISTORY:
        history.pop(0)
    return jsonify(result)


@app.route("/api/history")
def get_history():
    """Get historical readings."""
    return jsonify(history[-100:])


@app.route("/api/status")
def get_status():
    """System health check."""
    recent = history[-20:] if history else []
    anomaly_count = sum(1 for r in recent if r.get("is_anomaly"))
    return jsonify({
        "status": "critical" if anomaly_count > 5 else "warning" if anomaly_count > 2 else "healthy",
        "total_readings": len(history),
        "recent_anomalies": anomaly_count,
        "model_trained": detector.is_trained,
    })


if __name__ == "__main__":
    print("EdgeAI Monitor starting...")
    print(f"Model will auto-train after {RETRAIN_AT} live readings (~{RETRAIN_AT} seconds).")
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
