import Adafruit_DHT 

# =============================================================================
# Read sensor data ---
# =============================================================================
def read_sensor(sensor_pin): 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensor_pin) 
    return (humidity, temperature) 
