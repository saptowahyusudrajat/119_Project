import time
import requests
import Adafruit_DHT
import RPi.GPIO as GPIO

from RPi.GPIO import PWM

TOKEN = "YOUR_UBIDOTS_TOKEN"
DEVICE_LABEL = "demo"
TEMPERATURE_LABEL = "temperature"
HUMIDITY_LABEL = "humidity"
RAIN_LABEL = "rain"
LDR_LABEL = "ldr"
SERVO_PIN = 21   # GPIO pin number where the servo motor is connected
DHT_PIN = 4      # GPIO pin number where DHT11 sensor is connected
RAIN_SENSOR_PIN = 17   # GPIO pin number where rain sensor is connected
LDR_SENSOR_PIN = 18    # GPIO pin number where LDR sensor is connected

# Set up the servo motor
def setup_servo():
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo = PWM(SERVO_PIN, 50)  # Initialize PWM on servo pin with 50Hz frequency
    servo.start(0)  # Start PWM with a duty cycle of 0 (servo is in the closed position)
    return servo

# Control the servo to move to a specific angle
def move_servo(servo, angle):
    duty_cycle = 2.5 + (angle / 18)  # Convert angle to duty cycle (0-180 degrees)
    servo.ChangeDutyCycle(duty_cycle)

def read_dht11_data():
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    return temperature, humidity

def read_rain_sensor_data():
    GPIO.setup(RAIN_SENSOR_PIN, GPIO.IN)
    rain_data = GPIO.input(RAIN_SENSOR_PIN)
    return rain_data

def read_ldr_sensor_data():
    GPIO.setup(LDR_SENSOR_PIN, GPIO.IN)
    ldr_data = GPIO.input(LDR_SENSOR_PIN)
    return ldr_data

def send_to_ubidots(temperature, humidity, rain_data, ldr_data):
    payload = {
        TEMPERATURE_LABEL: temperature,
        HUMIDITY_LABEL: humidity,
        RAIN_LABEL: rain_data,
        LDR_LABEL: ldr_data
    }

    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Data sent to Ubidots: Temperature={temperature}, Humidity={humidity}, Rain={rain_data}, LDR={ldr_data}")
        else:
            print("Failed to send data. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    servo = setup_servo()  # Initialize the servo motor

    try:
        while True:
            temperature, humidity = read_dht11_data()
            rain_data = read_rain_sensor_data()
            ldr_data = read_ldr_sensor_data()
            if temperature is not None and humidity is not None:
                send_to_ubidots(temperature, humidity, rain_data, ldr_data)
            else:
                print("Failed to read DHT11 data.")
            
            # Control the servo based on LDR sensor data
            if ldr_data == 1:
                move_servo(servo, 0)  # Move servo to 0 degrees
            elif ldr_data == 0:
                move_servo(servo, 90)  # Move servo to 90 degrees

            time.sleep(2)  # Adjust the time interval as needed

    finally:
        servo.stop()  # Stop the servo PWM
        GPIO.cleanup()
