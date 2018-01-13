sensors = []
config = {}

def read_config():
    global sensors
    global config

    general_config_file = open("air_monitor.config")
    config = eval(general_config_file.read())
    print(config)
    
    temp_sensor_file = open("air_sensor.config");
    sensors = eval(temp_sensor_file.read()) 
    print(sensors)    



read_config()