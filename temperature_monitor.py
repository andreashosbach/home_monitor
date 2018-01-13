#!/usr/bin/python
 
from os import system 
from threading import Timer
from thingspeak import post_to_thingspeak_channel
from ds18b20 import read_sensor
from utils import trace

# =============================================================================
# Load drivers ---
# =============================================================================
system("modprobe w1-gpio")
system("modprobe w1-therm")

# =============================================================================
# Global variable declarations ---
# =============================================================================
config = {}
sensors = []

# =============================================================================
# Read configuration file
# =============================================================================
# Entry format: sensor_name=id
def read_config():
    global sensors
    global config

    general_config_file = open("temperature_monitor.config")
    config = eval(general_config_file.read())
    trace(config)
    
    sensor_config_file = open("temp_sensor.config")
    sensors = eval(sensor_config_file.read())
    trace(sensors)    
    

# =============================================================================
# Measure and write every x seconds
# =============================================================================
# Resets the timer
def measure():
    Timer(float(config["timer_wait"]), measure).start()
    
    measurements = []
    
    for sensor in sensors:
        temp = read_sensor(config["sensor_path"], sensor["id"])
        measurements.append({ "field" : sensor["field"], "value" : temp})

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