from os import system 
from datetime import datetime
from threading import Timer
import httplib
import urllib
import time
import sys

temp_sensors = []
config = {}

def read_config():
    global temp_sensors
    global config

    general_config_file = open("temperature_monitor.config")
    for line in general_config_file.readlines():
        splitted = line.split("=")
        config[splitted[0].strip()] = splitted[1].strip()
    
    sensor_config_file = open(config["sensor_config_file"])
    for line in sensor_config_file.readlines():
        splitted = line.split("=")
        temp_sensors.append([splitted[0].strip(), splitted[1].strip()])
        
        
        
def send_to_thingspeak(sensor_temp):
    if "thingspeak_channel_key" in config.keys():
        # use your API key generated in the thingspeak channels for the value of 'key'
        param_dict = {}
        for measurement in sensor_temp:
            param_dict[measurement[0]] = measurement[1]
        param_dict["key"] = config["thingspeak_channel_key"]
        params = urllib.urlencode(param_dict)
        print(params)    
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPSConnection("api.thingspeak.com")                
    else:
        print("Skipped sending to thingspeak")



read_config()
print(temp_sensors)
print(config)
sensor_temp = [["field1", 41.54], ["field2", 42.54]]
send_to_thingspeak(sensor_temp)

