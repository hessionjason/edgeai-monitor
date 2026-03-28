"""
EdgeAI Monitor configuration.

Centralizes all tunable parameters for sensor simulation,
anomaly detection, and the Flask application.
"""


class Config:
    # Flask
    DEBUG = True
    PORT = 5000

    # Sensor simulation
    SENSOR_BASELINE = {
        "temperature": 45.0,
        "voltage": 3.3,
        "memory": 42.0,
        "cpu": 25.0,
    }
    ANOMALY_INJECTION_RATE = 0.05

    # Anomaly detection
    ISOLATION_FOREST_ESTIMATORS = 100
    CONTAMINATION = 0.05
    TRAINING_SAMPLES = 300

    # Dashboard
    MAX_HISTORY = 200
    POLL_INTERVAL_MS = 1000
