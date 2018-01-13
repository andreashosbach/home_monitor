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
# Log Header
# =============================================================================
def create_log_header():
    log_header = "Datetime"
    for sensor in sensors:
        log_header = log_header + ";" + sensor[0]
    return log_header

# =============================================================================
# Reads all sensors and creates and writes a log entry
# =============================================================================
def create_log_entry(sensor_measurement):
    log_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for measurement in sensor_measurement:
        log_entry = log_entry + ";" + str(measurement[1])
        
    return log_entry
      
# =============================================================================
# Append a new line to the log file
# =============================================================================
def write_log(log_entry):
    if "local_data_file" in config.keys():
        logfile = open(config["local_data_file"], "a")
        logfile.write(log_entry + "\n")
        logfile.close()

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
    
    log_entry = create_log_entry(sensor_measurement)
    write_log(log_entry)
    send_to_thingspeak(sensor_measurement)
            
# =============================================================================
# Main ---
# =============================================================================
trace("Starting")
read_config()
log_header = create_log_header()
write_log(log_header)
trace("Running")
measure()        