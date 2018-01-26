import sys

# =============================================================================
# Global variable declarations ---
# =============================================================================
config = {}
sensors = []

# =============================================================================
# Read configuration file
# =============================================================================
# Entry format: sensor_name=id
def read_config():
    global config
    global sensors
    
    config_file_name = "monitor.config"
    if len(sys.argv) == 2:
        config_file_name = sys.argv[1]
    
    general_config_file = open(config_file_name)
    config = eval(general_config_file.read())
    sensors = config["sensors"]
    return config

# =============================================================================
# Check if a config value for a key exists
# =============================================================================
def has_config(key):
    return key in config.keys()
    
# =============================================================================
# Get config value for a key
# =============================================================================
def get_config(key):
    return config[key]

# =============================================================================
# Get configured sensors
# =============================================================================
def get_sensors():
    return sensors

