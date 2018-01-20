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
 