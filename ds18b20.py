import time
import datalogging
from datalogging import trace

# =============================================================================
# Read raw data from w1 device
# =============================================================================
def read_temperature_raw(sensor_path, sensor_id):
    sensor_file = open(sensor_path + sensor_id + "/w1_slave", "r")
    lines = sensor_file.readlines()
    sensor_file.close()
    return lines

# =============================================================================
# Read value of a temperature sensor_id
# =============================================================================
def read_sensor(sensor_path, sensor_id): 
    lines = read_temperature_raw(sensor_path, sensor_id)
    remaining_retry = 10
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temperature_raw(sensor_path, sensor_id)
        if remaining_retry == 0:
            trace("Sensor: " + str(sensor_id) + "read failed giving up", datalogging.ERROR)
            return 0.0
        else:
            trace("Sensor: " + str(sensor_id) + "read failed retry", datalogging.WARN)
            remaining_retry = remaining_retry - 1

    temp_output = lines[1].find("t=")

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_centigrade = float(temp_string) / 1000.0
        return temp_centigrade
