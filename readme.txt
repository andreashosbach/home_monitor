sudo nano /etc/defaults/keyboard
 -> change "gb" to "ch"
 
sudo raspi-config
 -> hostname (network)
 -> password
 -> ssh
 -> WiFi
 
sudo apt-get update

sudo apt-get install git 

Install Stuff for DHT22 Sensor:

On Pi:
sudo apt-get install python-dev 
sudo apt-get install python-pip 
git clone https://github.com/adafruit/Adafruit_Python_DHT.git 
cd Adafruit_Python_DHT 
sudo python setup.py install

If you use ds18b20 before starting:
sudo modprobe w1-gpio
sudo modprobe w1-therm
 
 
 
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
 