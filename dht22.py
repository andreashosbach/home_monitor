import Adafruit_DHT 
import datalogging
from datalogging import trace

# =============================================================================
# Read sensor data ---
# =============================================================================
def read_sensor(sensor_pin): 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensor_pin) 
    if humidity is None and temperature is None:
        trace("Failed to get reading on sensor: " + str(sensor_pin), datalogging.ERROR)

    return (temperature, humidity) 