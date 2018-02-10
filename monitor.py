#!/usr/bin/python

from threading import Timer
from config import get_config
from config import read_config
import sensors
import datalogging
import sys

def measure():
    # Measure and write every x seconds
    # Resets the timer
    Timer(float(get_config("timer_wait")), measure).start()
    
    measurements = sensors.measure() 
    datalogging.log(measurements)
    
def main():
    # Main
    print("Reading configuration")
    config_file_name = "monitor.config"
    if len(sys.argv) == 2:
        config_file_name = sys.argv[1]

    print(read_config(config_file_name))
    measure()        
    
# =============================================================================
if __name__ == "__main__":
    main()