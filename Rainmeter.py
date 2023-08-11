import RPi.GPIO as GPIO
import time

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
        else:
            print("No rain detected.")
        
        time.sleep(1)  # Wait for a second before reading again

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO configuration on program exit
