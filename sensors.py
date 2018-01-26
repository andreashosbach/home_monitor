from config import get_sensors
from config import get_config
import ds18b20
import dht22
from trace import trace
from trace import ERROR

# =============================================================================
# Read data from sensors
# =============================================================================
def measure():
    measurements = []
    
    for sensor in get_sensors():
        if sensor["type"] == "DHT22":
            temp, humidity = dht22.read_sensor(sensor["id"])
            if temp != None:
                measurements.append({ "field" : sensor["temperature"], "value" : temp})
            if humidity != None:
                measurements.append({ "field" : sensor["humidity"], "value" : humidity})
        elif sensor["type"] == "DS18B20":
            temp = ds18b20.read_sensor(get_config("DS18B20_sensor_path"), sensor["id"])
            if temp != None:
                measurements.append({ "field" : sensor["temperature"], "value" : temp})
        else:
            trace("Unknown sensor type: " + str(sensor), ERROR)

    return measurements