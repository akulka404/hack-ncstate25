import random
import time
import json
import paho.mqtt.client as mqtt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB Connection Setup
uri = "mongodb+srv://aniruddhak1911:CmACAFpIdTx2RsMy@cluster0.o8hkt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to MongoDB and select database & collection
try:
    client.admin.command('ping')
    print("Pinged your deployment. Successfully connected to MongoDB!")
    db = client["gridwise"]  # Database Name
    collection = db["energy_data"]  # Collection Name
except Exception as e:
    print(f"MongoDB Connection Error: {e}")

# MQTT Broker Setup
BROKER = "test.mosquitto.org"  # Public MQTT broker
TOPIC = "gridwise/energy"

mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, 1883, 60)

# Function to generate fake IoT energy data
def generate_fake_data():
    data = {
        "timestamp": int(time.time()),
        "household_id": "H001",
        "solar_output": round(random.uniform(0, 8), 2),  # kWh
        "energy_used": round(random.uniform(2, 10), 2),  # kWh
        "grid_voltage": round(random.uniform(220, 240), 2),  # V
        "current_draw": round(random.uniform(4, 8), 2)  # A
    }
    return data

# Publish & Store Data Loop
while True:
    energy_data = generate_fake_data()

    # Publish to MQTT
    mqtt_client.publish(TOPIC, json.dumps(energy_data))
    print(f"Published to MQTT: {energy_data}")

    # Store in MongoDB
    try:
        collection.insert_one(energy_data)
        print("Stored in MongoDB")
    except Exception as e:
        print(f"MongoDB Insertion Error: {e}")

    time.sleep(5)  # Adjust interval as needed
