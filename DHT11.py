import Adafruit_DHT
import time

# Set the sensor type (DHT11) and the GPIO pin number where the data pin is connected.
sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO pin number

while True:
    # Try to read the temperature and humidity data from the sensor.
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # If successful, print the data.
    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%')
    else:
        print('Failed to retrieve data from the sensor')

    # Wait for a few seconds before reading again.
    time.sleep(2)
