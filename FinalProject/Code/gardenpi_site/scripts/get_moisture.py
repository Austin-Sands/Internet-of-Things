#!/usr/bin/env python
import datetime
import time
import gpiozero
import mysql.connector

#####################################
# Mysql database connection and setup
gardenpidb = mysql.connector.connect(
    host="localhost",
    user="austin-sands",
    password="gardenpi_6551",
    database="gardenpidb",
)

curr_date = datetime.datetime.now()
formatted_date = curr_date.strftime('%Y-%m-%d %H:%M')

dbcursor = gardenpidb.cursor()

#relay variables
# relay1 is moisture sensor
relay_pin1 = 26
relay1 = gpiozero.OutputDevice(relay_pin1, active_high=False)

#moisture sensor variables
moisture_pin = 5
moisture_sensor = gpiozero.InputDevice(moisture_pin)
    
def get_moisture():

    #get moisture sensor reading and negate (raw input displays 1 if dry, we want it to display 0)
    is_moist = not moisture_sensor.value

    #send this data to the database
    sql_statement = "INSERT INTO moisture_data (date_time, reading, manual_read) VALUES (%s, %s, %s)"
    inputs = (formatted_date, is_moist, 1)

    dbcursor.execute(sql_statement, inputs)

    #if the moisture sensor is readying dry, turn on water pump and solenoid valve
    if not is_moist:
        give_water()

    return is_moist

def main():

    #turn on power to moisture sensor
    relay1.on()
    time.sleep(1)
    get_moisture()
    #turn off power to moisture sensor
    relay1.off()

    #commit modifications to database and close cursor and connection
    gardenpidb.commit()
    dbcursor.close()
    gardenpidb.close()


if __name__ == "__main__":
    main()