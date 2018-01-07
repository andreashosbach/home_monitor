#!/usr/bin/python
 
from os import system 
from datetime import datetime
from threading import Timer
import httplib
import urllib
import time

# =============================================================================
# Load drivers ---
# =============================================================================
system("modprobe w1-gpio")
system("modprobe w1-therm")

# =============================================================================
# Global variable declarations ---
# =============================================================================
config = {}
temp_sensors = []

# =============================================================================
# Read configuration file
# =============================================================================
# Entry format: sensor_name=id
def read_config():
    global temp_sensors
    global config

    general_config_file = open("temperature_monitor.config")
    for line in general_config_file.readlines():
        splitted = line.split("=")
        config[splitted[0].strip()] = splitted[1].strip()
    print(config)
    
    sensor_config_file = open("temp_sensor.config")
    for line in sensor_config_file.readlines():
        splitted = line.split("=")
        temp_sensors.append([splitted[0].strip(), splitted[1].strip()])
    print(temp_sensors)    
    
# =============================================================================
# Read raw data from w1 device
# =============================================================================
def temp_raw(sensor):
    f = open("/sys/bus/w1/devices/" + sensor + "/w1_slave", "r")
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
        lines = temp_raw()

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
    for sensor in temp_sensors:
        log_header = log_header + ";" + sensor[0]
    return log_header

# =============================================================================
# Reads all sensors and creates and writes a log entry
# =============================================================================
def create_log_entry(sensor_temp):
    log_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for measurement in sensor_temp:
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
    else:
        print("Skipped local logging")

# =============================================================================
# Measure and write every x seconds
# =============================================================================
# Resets the timer
def measure():
    Timer(float(config["timer_wait"]), measure).start()
    
    sensor_temp = []
    
    for sensor in temp_sensors:
        temp = read_temp(sensor[1])
        sensor_temp.append([sensor[0], temp])
    
    log_entry = create_log_entry(sensor_temp)
    write_log(log_entry)
    send_to_thingspeak(sensor_temp)
    
# =============================================================================
# Send to Thingspeak
# =============================================================================
def send_to_thingspeak(sensor_temp):
    # use your API key generated in the thingspeak channels for the value of 'key'
    measurement = sensor_temp[0]
    params = urllib.urlencode({measurement[0] : str(measurement[1]), "key" : config["thingspeak_channel_key"]})
    print(params)    
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPSConnection("api.thingspeak.com")                
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        print(data)
        conn.close()
    except:
        print("Connection to api.thingspeak.com failed")
            
# =============================================================================
# Main ---
# =============================================================================
print("Starting")
read_config()
log_header = create_log_header()
write_log(log_header)
print("Running")
measure()        