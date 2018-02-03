#!/usr/bin/python

from threading import Timer
from config import get_config
from config import read_config
import sensors
import datalogging

def measure():
    # Measure and write every x seconds
    # Resets the timer
    Timer(float(get_config("timer_wait")), measure).start()
    
    measurements = sensors.measure() 
    datalogging.log(measurements)
    
def main():
    # Main
    print("Reading configuration")
    print(read_config())
    measure()        
    
# =============================================================================
if __name__ == "__main__":
    main()