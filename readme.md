# Edge-to-Cloud AI Pipeline

A real-time Edge-to-Cloud AI pipeline for sensor monitoring, anomaly detection, and system observability.

The project collects sensor data at the edge, transfers it using MQTT, performs AI-based anomaly detection using Isolation Forest, containerizes the inference service with Docker, and exposes real-time metrics for monitoring through Prometheus and Grafana.

## Architecture

Sensor Data Generator
        |
        v
   MQTT / Mosquitto
        |
        v
 AI Inference Service
   (Isolation Forest)
        |
        v
 Prometheus Metrics
        |
        v
 Grafana Dashboard

## Features

- Real-time sensor data generation
- MQTT-based communication
- Temperature, humidity, and vibration monitoring
- AI-based anomaly detection using Isolation Forest
- Anomaly score calculation
- Inference latency measurement
- Docker containerization
- Prometheus metrics exposure
- Grafana real-time monitoring dashboard
- MAX/Mojo environment setup and feature-processing prototype

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Messaging | MQTT, Mosquitto |
| AI/ML | Scikit-learn, Isolation Forest |
| Containerization | Docker |
| Monitoring | Prometheus, Grafana |
| Edge Optimization | MAX, Mojo |
| Data Format | JSON |

## Project Structure

```text
Ecrio/
│
├── ai/
│   └── inference.py
│
├── edge/
│   └── sensor.py
│
├── mqtt/
│   └── subscriber.py
│
├── monitoring/
│   ├── prometheus.yaml
│   └── prometheus-local.yml
│
├── Dockerfile
├── README.md
└── .gitignore