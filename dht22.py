from Adafruit_DHT import read_retry 
from Adafruit_DHT import DHT22
from trace import trace
from trace import ERROR
def read_sensor(sensor_pin): 
    # Read sensor data
    humidity, temperature = read_retry(DHT22, sensor_pin) 
    if humidity is None and temperature is None:
        trace("Failed to get reading on sensor: " + str(sensor_pin), ERROR)

    return (temperature, humidity) 