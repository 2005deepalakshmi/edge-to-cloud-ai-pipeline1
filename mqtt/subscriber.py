import json
import signal
import sys
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "ecrio/edge/sensor"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
running = True

def signal_handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[SUBSCRIBER] Connected to broker {BROKER}:{PORT}")
        client.subscribe(TOPIC, qos=1)
        print(f"[SUBSCRIBER] Subscribed to topic '{TOPIC}'")
    else:
        print(f"[SUBSCRIBER] Connection failed with reason code {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"[SUBSCRIBER] Disconnected with reason code {reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(f"[SUBSCRIBER] Received -> device_id: {data.get('device_id')}, "
              f"temperature: {data.get('temperature')}, "
              f"humidity: {data.get('humidity')}, "
              f"vibration: {data.get('vibration')}, "
              f"timestamp: {data.get('timestamp')}")
    except json.JSONDecodeError:
        print(f"[SUBSCRIBER] Malformed JSON received: {msg.payload}")
    except Exception as e:
        print(f"[SUBSCRIBER] Error processing message: {e}")

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\n[SUBSCRIBER] Ctrl+C received, shutting down...")
except Exception as e:
    print(f"[SUBSCRIBER] Could not connect to broker: {e}")
    sys.exit(1)
finally:
    client.disconnect()
    print("[SUBSCRIBER] Disconnected cleanly.")
