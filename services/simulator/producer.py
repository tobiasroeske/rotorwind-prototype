import json
import random
import time
from datetime import datetime

# Import KafkaProducer from kafka library
from kafka import KafkaProducer


# --- Step 1: Configure the Kafka Producer ---
# - bootstrap_servers tells the producer where the Kafka broker is running
# - value_serializer converts Python dict -> JSON -> bytes
producer = KafkaProducer(
    bootstrap_servers="localhost:9094",  # Docker exposes Kafka on this port
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# --- Step 2: Define the Kafka topic name ---
TOPIC = "rotorwind.telemetry.v1"

# --- Step 3: Function to generate fake sensor data ---
def generate_sensor_data():
    return {
        "timestamp": datetime.utcnow().isoformat(),       # current UTC time
        "machine_id": "RW-001",                           # example machine id
        "temperature": round(random.uniform(20.0, 100.0), 2),  # random °C
        "vibration": round(random.uniform(0.0, 5.0), 2),       # random value
        "power_kw": round(random.uniform(100.0, 500.0), 2),    # random kW
    }

# --- Step 4: Main loop: send data every second ---
print(f"Starting producer, sending data to topic '{TOPIC}'...")

try:
    while True:
        data = generate_sensor_data()                  # create one message
        producer.send(TOPIC, value=data)               # send to Kafka
        print("Sent:", data)                           # log to console
        time.sleep(1)                                  # wait 1 second
except KeyboardInterrupt:
    print("Stopping producer...")

# --- Step 5: Cleanup ---
producer.close()