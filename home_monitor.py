import os
import time
from datetime import datetime

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")


temp_sensor1 = "28-000009aea5a6"
temp_sensor2 = "28-000009aeb943"

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

def write_log(log_entry):
    logfile = open("/home/pi/temp_monitor.csv", "a")
    logfile.write(log_entry + "\n")
    logfile.close()
    
    
def format_log_entry(time, col1, col2, col3, col4):
    return  time.strftime("%Y-%m-%d %H:%M:%S") + ";" + str(col1) + ";" + str(col2) + ";" + str(col3) + ";" + str(col4)

write_log("Time;"+ temp_sensor1 + ";" + temp_sensor2 + ";Spare;Spare")
while True:
        log_entry = format_log_entry(datetime.now(), read_temp(temp_sensor1), read_temp(temp_sensor2), "", "")
        print log_entry
        write_log(log_entry)
        time.sleep(1)    
        