import os
import json
import random
import time
import signal
import sys
from datetime import datetime, timezone

import numpy as np
import paho.mqtt.client as mqtt
from sklearn.ensemble import IsolationForest
from prometheus_client import start_http_server, Gauge, Counter


# =========================
# Configuration
# =========================

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
TOPIC = "ecrio/edge/sensor"

CONTAMINATION = 0.05
RANDOM_SEED = 42


# =========================
# Prometheus Metrics
# =========================

temperature_gauge = Gauge(
    "sensor_temperature",
    "Sensor temperature"
)

humidity_gauge = Gauge(
    "sensor_humidity",
    "Sensor humidity"
)

vibration_gauge = Gauge(
    "sensor_vibration",
    "Sensor vibration"
)

anomaly_score_gauge = Gauge(
    "anomaly_score",
    "AI anomaly score"
)

inference_latency_gauge = Gauge(
    "inference_latency_ms",
    "Inference latency in milliseconds"
)

anomaly_counter = Counter(
    "anomaly_total",
    "Total anomalies detected"
)


# Start Prometheus metrics server
start_http_server(8000)


# =========================
# MQTT Client
# =========================

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

running = True


# =========================
# Signal Handler
# =========================

def signal_handler(sig, frame):
    global running
    running = False


signal.signal(signal.SIGINT, signal_handler)


# =========================
# Generate Training Data
# =========================

def generate_training_data(n_samples=200):

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    temperature = np.random.uniform(
        20.0,
        45.0,
        n_samples
    )

    humidity = np.random.uniform(
        30.0,
        90.0,
        n_samples
    )

    vibration = np.random.uniform(
        0.0,
        1.0,
        n_samples
    )

    return np.column_stack(
        (
            temperature,
            humidity,
            vibration
        )
    )


# =========================
# Train Isolation Forest
# =========================

def train_model():

    print("[AI] Generating synthetic normal training data...")

    X_train = generate_training_data(
        n_samples=200
    )

    print(
        f"[AI] Training Isolation Forest on "
        f"{len(X_train)} samples..."
    )

    model = IsolationForest(
        contamination=CONTAMINATION,
        random_state=RANDOM_SEED
    )

    model.fit(X_train)

    print("[AI] Model training complete.")

    return model


model = train_model()


# =========================
# MQTT Connect
# =========================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):

    if reason_code == 0:

        print(
            f"[AI] Connected to broker "
            f"{MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}"
        )

        client.subscribe(
            TOPIC,
            qos=1
        )

        print(
            f"[AI] Subscribed to topic '{TOPIC}'"
        )

    else:

        print(
            f"[AI] Connection failed with "
            f"reason code {reason_code}"
        )


# =========================
# MQTT Disconnect
# =========================

def on_disconnect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):

    print(
        f"[AI] Disconnected with reason code "
        f"{reason_code}"
    )


# =========================
# MQTT Message Processing
# =========================

def on_message(
    client,
    userdata,
    msg
):

    global running

    if not running:
        return

    # -------------------------
    # Decode JSON
    # -------------------------

    try:

        payload = msg.payload.decode(
            "utf-8"
        )

        data = json.loads(payload)

    except json.JSONDecodeError:

        print(
            "[AI] Malformed JSON received, skipping."
        )

        return

    except Exception as e:

        print(
            f"[AI] Error decoding message: {e}"
        )

        return


    # -------------------------
    # Extract Sensor Data
    # -------------------------

    try:

        device_id = data.get(
            "device_id",
            "UNKNOWN"
        )

        temperature = data.get(
            "temperature"
        )

        humidity = data.get(
            "humidity"
        )

        vibration = data.get(
            "vibration"
        )

        timestamp = data.get(
            "timestamp",
            datetime.now(
                timezone.utc
            ).isoformat()
        )


        # Check missing values

        if (
            temperature is None
            or humidity is None
            or vibration is None
        ):

            print(
                "[AI] Missing sensor fields, skipping."
            )

            return


        # -------------------------
        # Prepare Features
        # -------------------------

        features = np.array(
            [[
                float(temperature),
                float(humidity),
                float(vibration)
            ]]
        )


        # -------------------------
        # AI Inference
        # -------------------------

        start_time = time.perf_counter()

        prediction = model.predict(
            features
        )[0]

        anomaly_score = model.decision_function(
            features
        )[0]

        end_time = time.perf_counter()


        latency_ms = (
            end_time - start_time
        ) * 1000


        # -------------------------
        # Prediction Label
        # -------------------------

        if prediction == -1:

            label = "ANOMALY"

        else:

            label = "NORMAL"


        # =========================
        # Update Prometheus Metrics
        # =========================

        temperature_gauge.set(
            float(temperature)
        )

        humidity_gauge.set(
            float(humidity)
        )

        vibration_gauge.set(
            float(vibration)
        )

        anomaly_score_gauge.set(
            float(anomaly_score)
        )

        inference_latency_gauge.set(
            float(latency_ms)
        )


        if label == "ANOMALY":

            anomaly_counter.inc()


        # =========================
        # Existing Terminal Output
        # =========================

        print(
            f"[AI] device_id: {device_id}"
        )

        print(
            f"[AI] temperature: {temperature}"
        )

        print(
            f"[AI] humidity: {humidity}"
        )

        print(
            f"[AI] vibration: {vibration}"
        )

        print(
            f"[AI] prediction: {label}"
        )

        print(
            f"[AI] anomaly_score: "
            f"{anomaly_score:.4f}"
        )

        print(
            f"[AI] inference_latency_ms: "
            f"{latency_ms:.4f}"
        )

        print(
            f"[AI] timestamp: {timestamp}"
        )

        print("-" * 50)


    except Exception as e:

        print(
            f"[AI] Error during inference: {e}"
        )


# =========================
# Register MQTT Callbacks
# =========================

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message


# =========================
# Start AI Service
# =========================

try:

    print(
        "[AI] Starting AI Inference Service..."
    )

    print(
        "[AI] Prometheus metrics available at "
        "http://localhost:8000/metrics"
    )

    client.connect(
        MQTT_BROKER_HOST,
        MQTT_BROKER_PORT,
        keepalive=60
    )

    client.loop_forever()


except KeyboardInterrupt:

    print(
        "\n[AI] Ctrl+C received, shutting down..."
    )


except Exception as e:

    print(
        f"[AI] Could not connect to broker: {e}"
    )

    sys.exit(1)


finally:

    client.disconnect()

    print(
        "[AI] Disconnected cleanly."
    )