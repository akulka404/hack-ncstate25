import random
import time
import json
import paho.mqtt.client as mqtt

BROKER = "mqtt://test.mosquitto.org"  # Public MQTT broker
TOPIC = "gridwise/energy"

def generate_fake_data():
    return {
        "timestamp": int(time.time()),
        "household_id": "H001",
        "solar_output": round(random.uniform(0, 8), 2),
        "energy_used": round(random.uniform(2, 10), 2),
        "grid_voltage": round(random.uniform(220, 240), 2),
        "current_draw": round(random.uniform(4, 8), 2)
    }

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

while True:
    data = generate_fake_data()
    client.publish(TOPIC, json.dumps(data))
    print(f"Published: {data}")
    time.sleep(5)
