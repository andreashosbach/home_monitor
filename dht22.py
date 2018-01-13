import Adafruit_DHT 

# =============================================================================
# Read sensor data ---
# =============================================================================
def read_sensor(sensor_pin): 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensor_pin) 
    if humidity is None and temperature is None:
        print("Failed to get reading on sensor: " + str(sensor_pin))

    return (humidity, temperature) 