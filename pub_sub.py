import paho.mqtt.client as mqtt
import time
import random

broker = "YOUR_PC_IP"
client_id = f'pi-{random.randint(0, 1000)}'
client = mqtt.Client(client_id)

# Callback function when the client receives a message
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Connect to the broker
client.connect(broker)

# Subscribe to a topic
client.subscribe("test/topic")

client.on_message = on_message

# Start the loop
client.loop_start()

# Publish messages
for i in range(10):
    message = f"Hello from {client_id} message {i}"
    client.publish("test/topic", message)
    time.sleep(2)

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()