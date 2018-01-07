temp_sensors = []
config = {}

def read_config():
    global temp_sensors
    global config

    sensor_config = open("temp_sensor.config")
    for line in sensor_config.readlines():
        splitted = line.split("=")
        temp_sensors.append([splitted[0].strip(), splitted[1].strip()])
        
    general_config = open("temperature_monitor.config")
    for line in general_config.readlines():
        splitted = line.split("=")
        config[splitted[0].strip()] = splitted[1].strip()
        
        
read_config()
print(temp_sensors)
print(config)
