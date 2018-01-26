#!/usr/bin/python

from threading import Timer
from config import get_config
from config import read_config
import actions
import sensors
import datalogging

# =============================================================================
# Measure and write every x seconds
# =============================================================================
# Resets the timer
def measure():
    Timer(float(get_config("timer_wait")), measure).start()
    
    measurements = sensors.measure() 
    datalogging.log(measurements)
    actions.run_actions(measurements)
    
# =============================================================================
# Main ---
# =============================================================================
def main():
    print("Reading configuration")
    print(read_config())
    measure()        
    
# =============================================================================
if __name__ == "__main__":
    main()