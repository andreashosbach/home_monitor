#!/usr/bin/python
 
from threading import Timer
from dht22 import read_sensor
from thingspeak import post_to_thingspeak_channel
from utils import trace

# =============================================================================
# Global variable declarations ---
# =============================================================================
config = {}
sensors = []

# =============================================================================
# Read configuration file
# =============================================================================
def read_config():
    global sensors
    global config

    general_config_file = open("air_monitor.config")
    config = eval(general_config_file.read())
    trace(config)
    
    sensor_config_file = open("air_sensor.config");
    sensors = eval(sensor_config_file.read())
    trace(sensors) 
    
# =============================================================================
# Measure and write every x seconds
# =============================================================================
# Resets the timer
def measure():
    Timer(float(config["timer_wait"]), measure).start()
    
    measurements = {}
    
    for sensor in sensors:
        humidity, temperature = read_sensor(sensor[1])
        measurements.append({"field" : sensor["temperature_field"], "value" : temperature})
        measurements.append({"field" : sensor["humidity_field"], "value" : humidity})
    
    if "thingspeak_channel_key" in config.keys():
        post_to_thingspeak_channel(measurements, config["thingspeak_channel_key"])
    else:
        trace(measurements)
            
# =============================================================================
# Main ---
# =============================================================================
def main():
    trace("Starting")
    read_config()
    trace("Running")
    measure()        

# =============================================================================
if __name__ == "__main__":
    main()
