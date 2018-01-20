#!/usr/bin/python
 
from os import system 
from threading import Timer
import sys
from datalogging import trace
import ds18b20
import dht22
import thingspeak

# =============================================================================
# Load drivers ---
# =============================================================================
system("sudo modprobe w1-gpio")
system("sudo modprobe w1-therm")

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
    global config
    global sensors
    
    config_file_name = "monitor.config"
    if len(sys.argv) == 2:
        config_file_name = sys.argv[1]
    
    general_config_file = open(config_file_name)
    config = eval(general_config_file.read())
    sensors = config["sensors"]
    trace(config)

# =============================================================================
# Measure and write every x seconds
# =============================================================================
# Resets the timer
def measure():
    Timer(float(config["timer_wait"]), measure).start()
    
    measurements = []
    
    for sensor in sensors:
        if sensor["type"] == "DHT22":
            temp, humidity = dht22.read_sensor(sensor["id"])
            if temp != None:
                measurements.append({ "field" : sensor["temperature"], "value" : temp})
            if humidity != None:
                measurements.append({ "field" : sensor["humidity"], "value" : humidity})
        elif sensor["type"] == "DS18B20":
            temp = ds18b20.read_sensor(config["DS18B20_sensor_path"], sensor["id"])
            if temp != None:
                measurements.append({ "field" : sensor["temperature"], "value" : temp})
        else:
            trace("Unknown sensor type: " + str(sensor))

    trace(measurements)
    if "thingspeak_channel_key" in config.keys():
        thingspeak.post_to_thingspeak_channel(measurements, config["thingspeak_channel_key"])
            
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