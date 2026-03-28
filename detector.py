"""
AI anomaly detection engine using Isolation Forest.

Trains on baseline embedded sensor data and scores new readings
to detect hardware anomalies in real time.
"""

import numpy as np
from sklearn.ensemble import IsolationForest


FEATURES = ["temperature", "voltage", "memory", "cpu"]


class AnomalyDetector:
    """Isolation Forest-based anomaly detector for embedded telemetry."""

    def __init__(self, contamination: float = 0.05):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
        )
        self.is_trained = False

    def train(self, readings: list[dict]) -> None:
        """Train the model on a batch of sensor readings."""
        X = self._extract_features(readings)
        self.model.fit(X)
        self.is_trained = True

    def predict(self, reading: dict) -> dict:
        """
        Score a single reading.

        Returns the reading augmented with:
          - anomaly_score: float (lower = more anomalous)
          - is_anomaly: bool
        """
        if not self.is_trained:
            reading["anomaly_score"] = 0.0
            reading["is_anomaly"] = False
            return reading

        X = self._extract_features([reading])
        score = self.model.decision_function(X)[0]
        label = self.model.predict(X)[0]

        reading["anomaly_score"] = round(float(score), 4)
        reading["is_anomaly"] = bool(label == -1)
        return reading

    def _extract_features(self, readings: list[dict]) -> np.ndarray:
        """Convert readings to feature matrix."""
        return np.array([[r[f] for f in FEATURES] for r in readings])
