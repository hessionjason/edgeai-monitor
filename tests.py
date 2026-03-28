"""
Unit tests for EdgeAI Monitor components.
"""

import unittest

from sensor import SensorSimulator
from detector import AnomalyDetector


class TestSensorSimulator(unittest.TestCase):

    def setUp(self):
        self.sensor = SensorSimulator()

    def test_single_reading_has_all_fields(self):
        reading = self.sensor.read()
        for key in ["timestamp", "temperature", "voltage", "memory", "cpu"]:
            self.assertIn(key, reading)

    def test_reading_values_are_numeric(self):
        reading = self.sensor.read()
        self.assertIsInstance(reading["temperature"], float)
        self.assertIsInstance(reading["voltage"], float)
        self.assertIsInstance(reading["memory"], float)
        self.assertIsInstance(reading["cpu"], float)

    def test_batch_returns_correct_count(self):
        batch = self.sensor.read_batch(50)
        self.assertEqual(len(batch), 50)

    def test_memory_and_cpu_within_bounds(self):
        for _ in range(100):
            reading = self.sensor.read()
            self.assertGreaterEqual(reading["memory"], 0)
            self.assertLessEqual(reading["memory"], 100)
            self.assertGreaterEqual(reading["cpu"], 0)
            self.assertLessEqual(reading["cpu"], 100)


class TestAnomalyDetector(unittest.TestCase):

    def setUp(self):
        self.sensor = SensorSimulator()
        self.detector = AnomalyDetector(contamination=0.05)

    def test_untrained_model_returns_no_anomaly(self):
        reading = self.sensor.read()
        result = self.detector.predict(reading)
        self.assertFalse(result["is_anomaly"])
        self.assertEqual(result["anomaly_score"], 0.0)

    def test_trained_model_returns_score(self):
        baseline = self.sensor.read_batch(200)
        self.detector.train(baseline)
        reading = self.sensor.read()
        result = self.detector.predict(reading)
        self.assertIn("anomaly_score", result)
        self.assertIn("is_anomaly", result)
        self.assertIsInstance(result["anomaly_score"], float)

    def test_extreme_reading_flagged_as_anomaly(self):
        baseline = self.sensor.read_batch(300)
        self.detector.train(baseline)
        extreme = {
            "timestamp": 0,
            "temperature": 200.0,
            "voltage": 0.1,
            "memory": 99.9,
            "cpu": 99.9,
        }
        result = self.detector.predict(extreme)
        self.assertTrue(result["is_anomaly"])


if __name__ == "__main__":
    unittest.main()
