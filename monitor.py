#!/usr/bin/python
 
from threading import Timer
import datalogging
from datalogging import trace
import ds18b20
#import dht22
import thingspeak
from config import has_config
from config import get_config
from config import get_sensors
from config import read_config


# =============================================================================
# Measure and write every x seconds
# =============================================================================
# Resets the timer
def measure():
    Timer(float(get_config("timer_wait")), measure).start()
    
    measurements = []
    
    for sensor in get_sensors():
        if sensor["type"] == "DHT22":
#            temp, humidity = dht22.read_sensor(sensor["id"])
            temp = 30.0
            humidity =70.0
            if temp != None:
                measurements.append({ "field" : sensor["temperature"], "value" : temp})
            if humidity != None:
                measurements.append({ "field" : sensor["humidity"], "value" : humidity})
        elif sensor["type"] == "DS18B20":
            temp = ds18b20.read_sensor(get_config("DS18B20_sensor_path"), sensor["id"])
            if temp != None:
                measurements.append({ "field" : sensor["temperature"], "value" : temp})
        else:
            trace("Unknown sensor type: " + str(sensor), datalogging.ERROR)

    trace(measurements, datalogging.INFO)
    if has_config("thingspeak_channel_key"):
        thingspeak.post_to_thingspeak_channel(measurements, get_config("thingspeak_channel_key"))
            
# =============================================================================
# Main ---
# =============================================================================
def main():
    print("Reading configuration")
    print(read_config())
    measure()        
    
# =============================================================================
if __name__ == "__main__":
    main()