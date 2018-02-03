import sys

config = {}
sensors = []

def read_config():
    # Read configuration file
    # Entry format: sensor_name=id
    global config
    global sensors
    
    config_file_name = "monitor.config"
    if len(sys.argv) == 2:
        config_file_name = sys.argv[1]
    
    general_config_file = open(config_file_name)
    config = eval(general_config_file.read())
    sensors = config["sensors"]
    return config

def has_config(key):
    # Check if a config value for a key exists
    return key in config.keys()
    
def get_config(key):
    # Get config value for a key
    return config[key]

def get_sensors():
    # Get configured sensors
    return sensors

