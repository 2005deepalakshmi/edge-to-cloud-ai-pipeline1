import json
import random
import time
import signal
import sys
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "ecrio/edge/sensor"
DEVICE_ID = "EDGE_01"
INTERVAL = 2

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
running = True

def signal_handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

def generate_payload():
    return json.dumps({
        "device_id": DEVICE_ID,
        "temperature": round(random.uniform(20.0, 45.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "vibration": round(random.uniform(0.0, 1.0), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[SENSOR] Connected to broker {BROKER}:{PORT}")
    else:
        print(f"[SENSOR] Connection failed with reason code {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"[SENSOR] Disconnected with reason code {reason_code}")

client.on_connect = on_connect
client.on_disconnect = on_disconnect

try:
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
except Exception as e:
    print(f"[SENSOR] Could not connect to broker: {e}")
    sys.exit(1)

print(f"[SENSOR] Publishing to topic '{TOPIC}' every {INTERVAL}s. Press Ctrl+C to stop.")

try:
    while running:
        payload = generate_payload()
        info = client.publish(TOPIC, payload, qos=1)
        info.wait_for_publish()
        print(f"[SENSOR] Published: {payload}")
        time.sleep(INTERVAL)
except Exception as e:
    print(f"[SENSOR] Error during publishing: {e}")
finally:
    client.loop_stop()
    client.disconnect()
    print("[SENSOR] Disconnected cleanly.")
