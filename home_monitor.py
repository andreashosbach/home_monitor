from os import system 
from datetime import datetime
from threading import Timer
import time

system("modprobe w1-gpio")
system("modprobe w1-therm")


temp_sensors = []
interval = 3

#name=id
def read_config():
    global temp_sensors
    config_file = open("temp_sensor.config")
    for line in config_file.readlines():
        splitted = line.split("=")
        temp_sensors.append([splitted[0].strip(), splitted[1].strip()])
    
def temp_raw(sensor):
    f = open("/sys/bus/w1/devices/" + sensor + "/w1_slave", "r")
    lines = f.readlines()
    f.close()
    return lines

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

def create_log_header():
    log_header = "Datetime"
    for sensor in temp_sensors:
        log_header = log_header + ";" + sensor[0]
    return log_header

def create_log_entry():
    log_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for sensor in temp_sensors:
        log_entry = log_entry + ";" + str(read_temp(sensor[1]))
        
    return log_entry
      
def write_log(log_entry):
    logfile = open("/home/pi/temp_monitor.csv", "a")
    logfile.write(log_entry + "\n")
    logfile.close()

def measure():
    print("Measure")
    Timer(5.0, measure).start()
    log_entry = create_log_entry()
    write_log(log_entry)
    
# Main
print("Starting")
read_config()
log_header = create_log_header()
write_log(log_header)
print("Running")
measure()        