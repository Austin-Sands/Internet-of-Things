#!/usr/bin/env python
import datetime
import time
import gpiozero
import mysql.connector
import os
import shutil

from picamera2 import Picamera2
from w1thermsensor import W1ThermSensor
from smbus import SMBus

#####################################
# Mysql database connection and setup
gardenpidb = mysql.connector.connect(
    host="localhost",
    user="austin-sands",
    password="gardenpi_6551",
    database="gardenpidb",
)

curr_date = datetime.datetime.now()
curr_hour = curr_date.hour
formatted_date = curr_date.strftime('%Y-%m-%d %H:%M')

dbcursor = gardenpidb.cursor()
#####################################
# Python implementation

#temp sensor variables
temp_sensor = W1ThermSensor()

#light resistor variables
bus = SMBus(1)
adc = 0x4b
ldr = 0x84

#relay variables
# relay1 is moisture sensor, relay2 is pump, relay3 is solenoid valve
relay_pin1 = 26
relay1 = gpiozero.OutputDevice(relay_pin1, active_high=False)
relay_pin2 = 20
relay2 = gpiozero.OutputDevice(relay_pin2, active_high=False)
relay_pin3 = 21
relay3 = gpiozero.OutputDevice(relay_pin3, active_high=False)

#moisture sensor variables
moisture_pin = 5
moisture_sensor = gpiozero.InputDevice(moisture_pin)

#watering interval in seconds
water_time = 5

#setup camera
camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": (600,480)})
camera.configure(camera_config)
img_filepath = "/var/www/gardenpi.com/public_html/images/" + formatted_date + ".jpg"
most_recent_filepath = "/var/www/gardenpi.com/public_html/images/recent.jpg"

def get_temp():
    current_temp = temp_sensor.get_temperature()
    current_temp = (current_temp * 9 / 5) + 32

    #sql statement to pass data to proper DB table
    sql_statement = "INSERT INTO temp_data (date_time, reading, manual_read) VALUES (%s, %s, %s)"
    inputs = (formatted_date, current_temp, 0)

    dbcursor.execute(sql_statement, inputs)

    return current_temp

def get_light():
    bus.write_byte(adc, ldr)
    result = bus.read_byte(adc)

    #sql statement to pass data to proper DB table
    sql_statement = "INSERT INTO light_data (date_time, reading, manual_read) VALUES (%s, %s, %s)"
    inputs = (formatted_date, result, 0)

    dbcursor.execute(sql_statement, inputs)

    return result
    
def get_moisture():

    #get moisture sensor reading and negate (raw input displays 1 if dry, we want it to display 0)
    is_moist = not moisture_sensor.value

    #send this data to the database
    sql_statement = "INSERT INTO moisture_data (date_time, reading, manual_read) VALUES (%s, %s, %s)"
    inputs = (formatted_date, is_moist, 0)

    dbcursor.execute(sql_statement, inputs)

    #if the moisture sensor is readying dry, turn on water pump and solenoid valve
    if not is_moist:
        give_water()

    return is_moist

def give_water():
    #send data to database
    sql_statement = "INSERT INTO watering_log (date_time, manual_call) VALUES (%s, %s)"
    inputs = (formatted_date, 0)

    dbcursor.execute(sql_statement, inputs)

    #turn on pump relay to send power to pump
    relay2.on()
    #turn on solenoid valve relay
    relay3.on()
    time.sleep(water_time)
    #turn off relays
    relay2.off()
    relay3.off()

def take_picture():
    #check hour of day, no point to take picture if it's pitch black
    if(curr_hour > 7 and curr_hour < 20):
        #take image with camera
        camera.start_and_capture_file(img_filepath,  capture_mode=camera_config, show_preview=False)
        #overwrite "recent.jpg" with new image so server knows which to display
        shutil.copyfile(img_filepath, most_recent_filepath)


def main():

    take_picture()

    #turn on power to moisture sensor
    relay1.on()
    print("Current temp: ", get_temp())
    print("Current light: ", get_light())
    print("Moisture detected: ", get_moisture())
    #turn off power to moisture sensor
    relay1.off()

    #commit modifications to database and close cursor and connection
    gardenpidb.commit()
    dbcursor.close()
    gardenpidb.close()


if __name__ == "__main__":
    main()