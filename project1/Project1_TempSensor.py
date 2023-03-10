"""
File:   Project1_TempSensor.py
Author: Austin Sands
Date:   02/10/2023
Description: This python script was written and tested on a Raspberry Pi 3B. 
This program requires one LED connected to GPIO18 (physical pin 12) as well as a 
DS18B20 temperature sensor with the data line connected to GPIO4 (physical pin 7).
"""

from gpiozero import LED
import time
import os
import glob

#declare LED position
led = LED(18)

"""
Declare variables and functions for DS18B20
"""
#variable to hold temperature
temperature = 0.0

#set temperature threshold desired (default in Fahrenheit, if you wish to use celcius ensure you're 
# passing false in the get_temp parameters)
temp_threshold = 75

#start modules for thermal sensor
os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

#declare directory for devices to access sensor
dir_base = "/sys/bus/w1/devices/"
device_folder = glob.glob(dir_base + "28*")[0]
device_file = device_folder + "/w1_slave"

#function will open the sensor given with directory and read raw data from probe
def get_raw_temp():
    sensor = open(device_file, "r")
    data = sensor.readlines()
    sensor.close()
    return data

def get_temp(fahrenheit = True):
    data = get_raw_temp()

    #remove whitespace from line and if last three characters aren't YES print no temp read
    #YES indicates that the probe is reading a temperature
    if data[0].strip()[-3:] != "YES":
        print("Error: No temp read!\n")
    else:
        #if YES in first line, search second line for "t=" and read temperature value from
        # 2 positions to the right of the "t"
        temp_position = data[1].find("t=")

        #if "t=" are last two strings in the line, do not record blank temp data
        if temp_position != -1:
            #actual temp data is 2 positions to right of "t" and remaining
            temp_string = data[1][temp_position+2:]
            #divide by 1000 to get celcius from raw data
            temp_c = float(temp_string) / 1000

            #if fahrenheit param is passed as false, just return celcius
            #this is not utilized in this project but I figured it would be useful if I want 
            #to recycle this code for later project and use this functionality
            if not fahrenheit:
                return temp_c

            #if fahrenheit is true (default value true) calculate fahrenheit and return
            temp_f = (temp_c * 1.8) + 32
            return temp_f
            
"""
End variables and functions for DS18B20
"""

while True:
    temperature = get_temp()

    print("Temp: " + str(temperature) + "F\n")

    if temperature > temp_threshold:
        led.on()
        print("Temp is past limit!")
    else:
        led.off()

    #only read the temp every one second. I could do this in the get_temp function but I
    #don't want to add a sleep call in the code in case I use the function in the future
    #and don't want it to mess with any loops
    time.sleep(1)
