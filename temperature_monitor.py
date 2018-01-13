#!/usr/bin/python
 
from os import system 
from datetime import datetime
from threading import Timer
import httplib
import urllib
import time
import sys

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
# Write a formatted trace line
# =============================================================================
def trace(line):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + str(line))
    sys.stdout.flush()

# =============================================================================
# Read configuration file
# =============================================================================
# Entry format: sensor_name=id
def read_config():
    global sensors
    global config

    general_config_file = open("temperature_monitor.config")
    for line in general_config_file.readlines():
        splitted = line.split("=")
        config[splitted[0].strip()] = splitted[1].strip()
    trace(config)
    
    sensor_config_file = open(config["sensor_config_file"])
    for line in sensor_config_file.readlines():
        splitted = line.split("=")
        sensors.append([splitted[0].strip(), splitted[1].strip()])
    trace(sensors)    
    
# =============================================================================
# Read raw data from w1 device
# =============================================================================
def temp_raw(sensor):
    f = open(config["sensor_path"] + sensor + "/w1_slave", "r")
    lines = f.readlines()
    f.close()
    return lines

# =============================================================================
# Read value of a temperature sensor
# =============================================================================
def read_temp(sensor): 
    lines = temp_raw(sensor)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = temp_raw(sensor)

    temp_output = lines[1].find("t=")

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# =============================================================================
# Send to Thingspeak
# =============================================================================
def send_to_thingspeak(sensor_measurement):
    if "thingspeak_channel_key" in config.keys():
        param_dict = {}
        for measurement in sensor_measurement:
            param_dict[measurement[0]] = measurement[1]
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
    
    sensor_measurement = []
    
    for sensor in sensors:
        temp = read_temp(sensor[1])
        sensor_measurement.append([sensor[0], temp])
    
    send_to_thingspeak(sensor_measurement)
            
# =============================================================================
# Main ---
# =============================================================================
trace("Starting")
read_config()
log_header = create_log_header()
trace("Running")
measure()        