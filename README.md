# EdgeAI Monitor

Real-time system monitoring dashboard with AI-powered anomaly detection.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6-orange)

## Overview

EdgeAI Monitor reads live hardware telemetry from your machine — CPU temperature, CPU load, memory usage, and battery voltage — and applies an Isolation Forest ML model to detect anomalies in real time. When your system behaves unusually (e.g. a CPU spike or memory surge), the AI flags it on the dashboard.

## Features

- Real system metrics via `psutil` (CPU, memory, battery) — not simulated
- AI anomaly detection using Isolation Forest (unsupervised ML)
- Real-time web dashboard with auto-refreshing Chart.js graphs
- Anomaly logging with live alerts
- REST API for integration with external systems

## Quick Start

```bash
# Clone the repo
git clone https://github.com/hessionjason/edgeai-monitor.git
cd edgeai-monitor

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python3 app.py
```

Open `http://localhost:8080` in your browser.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/data` | GET | Latest sensor readings + anomaly scores |
| `/api/history` | GET | Historical data (last 100 readings) |
| `/api/status` | GET | System health status |

## How It Works

1. **Real Sensor Data** - Reads actual CPU load, memory usage, battery voltage, and CPU temperature from the host machine using `psutil`
2. **AI Anomaly Detection** - On startup, the app collects 50 baseline readings to train an Isolation Forest model. It learns what "normal" looks like for your system, then scores every new reading in real time
3. **Live Dashboard** - Flask serves a responsive dark-themed UI that polls the API every second and renders live charts with anomaly highlighting

## Architecture

```
edgeai-monitor/
├── app.py              # Flask app + API routes
├── sensor.py           # Real system metrics reader (psutil)
├── detector.py         # AI anomaly detection engine
├── config.py           # Tunable parameters
├── tests.py            # Unit tests
├── templates/
│   └── dashboard.html  # Web dashboard UI
└── requirements.txt
```

## License

MIT
