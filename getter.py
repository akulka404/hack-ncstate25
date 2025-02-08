import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "gridwise/energy"

def on_message(client, userdata, message):
    print(f"Received: {message.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

client.loop_forever()