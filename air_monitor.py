#!/usr/bin/python
 
from datetime import datetime
from threading import Timer
import httplib
import urllib
import sys
import Adafruit_DHT 
 
# =============================================================================
# Global variable declarations ---
# =============================================================================
config = {}
sensors = []

# =============================================================================
# Write a formatted trace line
# =============================================================================
def trace(line):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + str(line))
    sys.stdout.flush()

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
# Read sensor data ---
# =============================================================================
def read_sensor(sensor_pin): 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensor_pin) 
    return (humidity, temperature) 
    
# =============================================================================
# Send to Thingspeak
# =============================================================================
def send_to_thingspeak(measurements):
    if "thingspeak_channel_key" in config.keys():
        param_dict = {}
        for measurement in measurements:
            param_dict[measurement["field"]] = measurement["value"]
        param_dict["key"] = config["thingspeak_channel_key"]
        params = urllib.urlencode(param_dict)

        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPSConnection("api.thingspeak.com")                

        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            trace([response.status, response.reason, data])
            conn.close()
        except:
            trace("Sending to Thingspeak failed")

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
    
    send_to_thingspeak(measurements)
            
# =============================================================================
# Main ---
# =============================================================================
trace("Starting")
read_config()
trace("Running")
measure()        

