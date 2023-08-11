import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt


# MQTT broker details
broker_address = "broker.hivemq.com"  # Replace with your MQTT broker address
broker_port = 1883  # Default MQTT port

# Create an MQTT client
client = mqtt.Client("publisher")

# Connect to the broker
client.connect(broker_address, broker_port)

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the rain sensor's DO pin
rain_sensor_pin = 17

# Set up the GPIO pin for input
GPIO.setup(rain_sensor_pin, GPIO.IN)

try:
    while True:
        # Read the digital value from the rain sensor
        rain_value = GPIO.input(rain_sensor_pin)
        
        if rain_value == GPIO.LOW:
            print("It's raining!")
            message = f"Hujan bos!"
        else:
            message = f"Cuaca cerah!"
            print("No rain detected.")

        topic = "topicSIC/MQTTdemo"
        client.publish(topic, message)        
        time.sleep(1)  # Wait for a second before reading again

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO configuration on program exit
