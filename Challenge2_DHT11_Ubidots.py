import time
import requests
import Adafruit_DHT

TOKEN = "BBFF-HRGwpx4IeRlvLnblG1tRny0YehPjWz"
DEVICE_LABEL = "demo"
TEMPERATURE_LABEL = "temperature"
HUMIDITY_LABEL = "humidity"
DHT_PIN = 4  # GPIO pin number where DHT11 sensor is connected

def read_dht11_data():
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    return temperature, humidity

def send_to_ubidots(temperature, humidity):
    payload = {
        TEMPERATURE_LABEL: temperature,
        HUMIDITY_LABEL: humidity
    }

    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    try:
        response = requests.post(url=url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Data sent to Ubidots: Temperature={temperature}, Humidity={humidity}")
        else:
            print("Failed to send data. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)

if __name__ == "__main__":
    while True:
        temperature, humidity = read_dht11_data()
        if temperature is not None and humidity is not None:
            send_to_ubidots(temperature, humidity)
        else:
            print("Failed to read DHT11 data.")

        time.sleep(2)  # Adjust the time interval as needed
