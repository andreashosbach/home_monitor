# Home Monitor

Read from different sensors and push the data to thingspeak

## Getting Started

You will need a thingspeak account. 
Add the write keys and field id's to the config in the display.config


### Prerequisites

You will need a rasperry pi 


### Installing

sudo nano /etc/defaults/keyboard
 -> change "gb" to "ch"
 
- sudo raspi-config
 -> hostname (network)
 -> password
 -> ssh
 -> WiFi
 
- sudo apt-get update
- sudo apt-get install git 

Install Stuff for DHT22 Sensor:
On Pi:
- sudo apt-get install python-dev 
- sudo apt-get install python-pip 
- git clone https://github.com/adafruit/Adafruit_Python_DHT.git 
- cd Adafruit_Python_DHT 
- sudo python setup.py install

- clone the home_monitor repository

- If you use ds18b20 before starting:
  sudo modprobe w1-gpio
  sudo modprobe w1-therm
 
- start with: python display.py > display.log &
 
 
 Full config file options:
 
 {
  "timer_wait": 60.0,
  "DS18B20_sensor_path" : "/sys/bus/w1/devices/"", 
  "trace_level" : "INFO",
  "sensors" :
  [
    {"type" : "DHT22", "id" : "23", "temperature" : "field1", "humidity" : "field2"},
    {"type" : "DS18B20", "id" :"28-000009aea5a6", "temperature" :  "field4"},
  ],
  "logging" :
  {
    "trace" : {"level" : "ALWAYS"},
    "thingspeak" : {"channel_key" : "CAFFEECAFFEECAFF"}
  }, 
  "actions" :
  [
    {"type" : "TRACE", "condition" : "val['field4'] > 40", "level" : "WARN"} 
  ] 
}
 

To have it start when the raspberry is powered on, create a script home_monitor.sh with the following content in /etc/init.d (do this as user root, with: sudo nano home_display.sh):
 
 #! /bin/sh
 cd [source directory]/home_monitor
 python monitor.py > monitor.log
 
make the script executable with: sudo chmod 755 home_display.sh
add this script to the start with:  sudo update-rc.d home_monitor.sh defaults
 
## Running the tests

There are currently no tests :P

## Deployment

Clone and run...

## Authors

* **Andreas Hosbach** - [AndreasHosbach](https://github.com/AndreasHosbach)

See also the list of [contributors](https://github.com/AndreasHosbach/home_display/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who wrote tutorials about raspberry pi.
